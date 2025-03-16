from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from news.resources import POSITIONS
from django.utils.translation import gettext as _

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    def __str__(self):
        return self.user.username
    def update_rating(self):
        #суммарный рейтинг каждой статьи автора умножается на 3;
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        #суммарный рейтинг всех комментариев автора;
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        #суммарный рейтинг всех комментариев к статьям автора.
        comment_to_post_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_rating + comment_rating + comment_to_post_rating
        self.save()
        return self.rating



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Category Name'))
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)
    def __str__(self):
        return self.name
class Post(models.Model):
    author=models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    post_type=models.CharField(max_length=7, choices=POSITIONS, verbose_name=_('Type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication Date'))
    categories=models.ManyToManyField(Category, through='PostCategory', verbose_name=_('Categories'))
    title=models.CharField(max_length=255, verbose_name=_('Title'))
    text=models.TextField(verbose_name=_('Text'))
    rating=models.IntegerField(default=0, verbose_name=_('Rating'))

    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'
    def get_absolute_url(self):
        return reverse('news:about_new', kwargs={'pk': self.pk})

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    text = models.TextField(verbose_name=_('Text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication Date'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

