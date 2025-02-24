from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post
from .tasks import send_notif, send_UPGRADE_notif


@receiver(m2m_changed, sender=Post.categories.through)
def new_post(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.categories.all()
        subscribers = set()
        for category in categories:
            subscribers.update(category.subscribers.all())
            
        for subscriber in subscribers:
            if subscriber.email:
                category_names = ', '.join([category.name for category in categories])
                send_notif.delay(subscriber.email, instance.title, instance, category_names)

@receiver(post_save, sender=Post)
def upgrade_new(sender, instance, created, **kwargs):
    if not created:
        categories = instance.categories.all()
        subscribers = set()
        for category in categories:
            subscribers.update(category.subscribers.all())
            
        for subscriber in subscribers:
            if subscriber.email:
                send_UPGRADE_notif.delay(subscriber.email, instance.title, instance)

@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = f'post_{instance.pk}'
    cache.delete(cache_key)

@receiver(post_delete, sender=Post)
def clear_post_cache_on_delete(sender, instance, **kwargs):
    cache_key = f'post_{instance.pk}'
    cache.delete(cache_key)