from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemGraph.settings')

app = Celery('SystemGraph', broker='amqp://guest@localhost//', backend='amqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))