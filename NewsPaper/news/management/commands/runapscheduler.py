import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from datetime import timedelta
from news.models import Post
from django.core.mail import send_mail
 
 
logger = logging.getLogger(__name__)
 
 
def my_job():
    one_week_ago = timezone.now() - timedelta(weeks=1)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago)
    for post in new_posts:
        for subscriber in post.categories.values_list('subscribers__email', flat=True):  # Предполагается, что у вас есть связь с подписчиками
            if subscriber:
                send_mail(
                    subject=f'Новый пост: {post.title}',
                    message=f'Будьте одним из первых: {post.get_absolute_url()}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber],
                )
 
 
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
