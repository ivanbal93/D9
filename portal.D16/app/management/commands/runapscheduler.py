import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from app.models import Category, Post, User
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail
 
 
logger = logging.getLogger(__name__)
 
end_date = datetime.now(tz=timezone.utc)
start_date = end_date - timedelta(days=7)
list_of_posts = Post.objects.filter(post_datetime__lte=end_date, post_datetime__gte=start_date).values()
def my_job():
    for category in Category.objects.all().values('category_name', 'subscribers'):
        msg = ''
        rcp_l = []
        for post in list_of_posts:
            if post['category'] == category['category_name']:
                link = f"http://127.0.0.1:8000/news/{post['id']}"
                msg += f"{link}/n{post['post_header']}/n"
                rcp_l.append(User.objects.get(id=category['subscribers']).email)
        

        send_mail(
            subject='News of the last week from your favorite category ',
            message=msg,
            from_email=None,
            recipient_list=rcp_l
        )

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="10", minute="00"
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