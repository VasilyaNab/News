from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils import timezone
from django.conf import settings
from .models import Author, Post, Category
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})


class SubscribeView(View):
    def get(self, request, category_id):
        category = Category.objects.filter(id=category_id).first()
        is_subscribed = request.user.is_authenticated and category.subscribers.filter(id=request.user.id).exists()
        return render(request, 'subscribe.html', {
            'category': category,
            'is_subscribed': is_subscribed,
        })

    def post(self, request, category_id):
        category = Category.objects.filter(id=category_id).first()
        user = request.user

        if user.is_authenticated:
            if category.subscribers.filter(id=user.id).exists():
                category.subscribers.remove(user)
                is_subscribed = False
                message = f"Здравствуйте, {user.username}!\nК сожалению, вы отписались от новостей в категории {category.name}.\n\nНадеюсь вы еще вернетесь и найдете категорию, которая вам по душе."
            else:
                category.subscribers.add(user)
                is_subscribed = True
                message = f"Здравствуйте, {user.username}!\nВы успешно подписались на новости в категории {category.name}. Ждем новых новостей!\n\nРады что вы с нами!"

            subject = f"Категория: {category.name}"
            email = user.email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            msg.send()

        return redirect('news:subscribe', category_id=category.id)
@method_decorator(cache_page(60 * 5), name='dispatch')
class NewsList(ListView):
    model = Post
    ordering = '-created_at' 
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.all()
        return context

@method_decorator(cache_page(60 * 5), name='dispatch')
class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
    def get_object(self, queryset=None):
        cache_key = f'post_{self.kwargs["pk"]}'
        post = cache.get(cache_key)

        if not post:
            post = super().get_object(queryset)
            cache.set(cache_key, post)

        return post
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/admin/'
    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def form_valid(self, form):
            author, created = Author.objects.get_or_create(user=self.request.user)
            publish_limit = Post.objects.filter(author=author, created_at__date=timezone.now().date()).count()
            if publish_limit >= 3:
                return render(self.request, 'limit.html')
            form.instance.author = author
            form.instance.post_type = self.kwargs.get('post_type', 'news')
            post = form.save()
            categories = form.cleaned_data.get('categories')
            post.categories.set(categories)
            return redirect('news:news_list')
                
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()
    def form_valid(self, form):
        form.instance.post_type = self.kwargs.get('post_type', 'news')
        post = form.save()
        return redirect('news:news_list')

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news:news_list')