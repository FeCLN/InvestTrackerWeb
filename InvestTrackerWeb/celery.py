from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InvestTrackerWeb.settings')

app = Celery('InvestTrackerWeb')  

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task():
    print('Request: {0!r}'.format(self.request))