from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post


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
                subject = f'Новая новость в категории {category_names}: {instance.title}'
                html_content = render_to_string('message.html', {'post': instance})

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

@receiver(post_save, sender=Post)
def upgrade_new(sender, instance, created, **kwargs):
    if not created:
        categories = instance.categories.all()
        subscribers = set()
        for category in categories:
            subscribers.update(category.subscribers.all())
            
        for subscriber in subscribers:
            if subscriber.email:
                subject = f'Пост был обновлен: {instance.title}'
                html_content = render_to_string('messageUPGRADE.html', {'post': instance})

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

