from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils import timezone, translation
from django.conf import settings
from .models import Author, Post, Category
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
import logging
import pytz

logger = logging.getLogger(__name__)

class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        current_time = getattr(request, 'current_time', None)

        return render(request, 'category_list.html', {
            'categories': categories,
            'current_time': current_time,
        })


class SubscribeView(View):
    def get(self, request, category_id):
        category = Category.objects.filter(id=category_id).first()
        is_subscribed = request.user.is_authenticated and category.subscribers.filter(id=request.user.id).exists()
        current_time = getattr(request, 'current_time', None)
        return render(request, 'subscribe.html', {
            'category': category,
            'is_subscribed': is_subscribed,
            'current_time': current_time,
        })

    def post(self, request, category_id):
        category = Category.objects.filter(id=category_id).first()
        user = request.user

        if user.is_authenticated:
            if category.subscribers.filter(id=user.id).exists():
                category.subscribers.remove(user)
                is_subscribed = False
                message = _("Hello, %(username)s!\nUnfortunately, you have unsubscribed from news in the category %(category_name)s.\n\nI hope you will return and find a category that you like.") % {'username': user.username, 'category_name': category.name}
            else:
                category.subscribers.add(user)
                is_subscribed = True
                message = _("Hello, %(username)s!\nYou have successfully subscribed to news in the category %(category_name)s. We look forward to new news!\n\nWe are glad to have you with us!") % {'username': user.username, 'category_name': category.name}

            subject = _("Category: %(category_name)s") % {'category_name': category.name}
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

    def post(self, request, *args, **kwargs):
        tz = request.POST.get('timezone')
        if tz:
            request.session['django_timezone'] = tz
            timezone.activate(pytz.timezone(tz))
        return redirect('news:news_list')
    def get(self, request, *args, **kwargs):
        language = request.GET.get('language')
        if language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = PostFilter(self.request.GET, queryset=self.get_queryset())
        filterset.form.fields['title'].label = translation.gettext('Enter the title')
        filterset.form.fields['author'].label = translation.gettext('Author')
        filterset.form.fields['created_at'].label = translation.gettext('Publication date')
        context['filterset'] = filterset
        context['categories'] = Category.objects.all()
        context['timezones'] = pytz.common_timezones

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
        post = form.save()
        return redirect('news:news_list')

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news:news_list')


def my_view(request):
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")