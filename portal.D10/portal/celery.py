import os
from celery import Celery
from app.management.commands import runapscheduler
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
 
app = Celery('portal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

#  уведомление о новых новостях по понедельникам
app.conf.beat_schedule = {
    'news_every_monday': {
        'tasl': runapscheduler,
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    }
}