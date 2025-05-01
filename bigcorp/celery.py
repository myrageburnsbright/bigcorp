import os

from celery import Celery
from celery.schedules import crontab 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigcorp.settings')

app = Celery('bigcorp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-spam-every-10-seconds': {
#         'task': 'payment.tasks.send_spam_email',
#         'schedule': crontab(minute='*/1'),
#     },
# }