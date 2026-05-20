import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlc_eats.settings')

app = Celery('tlc_eats')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()