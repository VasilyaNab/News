from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_all_newss():
    last_3_news = Post.objects.filter(created_at__gte=timezone.now() - timedelta(weeks=1)).order_by('-created_at')[:3]
    users = User.objects.all()
    context = {
        'last_3_news': last_3_news,
    }
    html_content = render_to_string('emailmessage/sending_all_news.html', context)
    for user in users:
        if user.email:
            subject = 'Еженедельная рассылка новостей'
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()