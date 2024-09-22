from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgsos.settings')

app = Celery('bgsos')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(15.0, my_periodic_task.s(), name='Run every 15 seconds')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
