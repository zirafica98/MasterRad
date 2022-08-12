import os
from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

os.environ.setdefault('DJANGO_SETINGS_MODULE','mysite.settings')

app = Celery('myshop')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()