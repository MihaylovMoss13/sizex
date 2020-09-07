import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sizex.settings')

from django.conf import settings

app = Celery('sizex')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
