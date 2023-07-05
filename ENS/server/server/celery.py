from __future__ import absolute_import
import os
from celery import Celery
from kombu import Queue
from server.settings import base

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.development')

app = Celery('server')

default_queue = Queue('default', routing_key='default')
low_priority_queue = Queue('low_priority_queue', routing_key='low_priority')
high_priority_queue = Queue('high_priority_queue', routing_key='high_priority')

app.conf.task_queues = [
    default_queue,
    low_priority_queue,
    high_priority_queue,
]

# app.conf.task_queues = {
#     'default': {
#         'exchange': 'default',
#         'exchange_type': 'direct',
#         'routing_key': 'default',
#     },
#     'low_priority_queue': {
#         'exchange': 'low_priority_queue',
#         'exchange_type': 'direct',
#         'routing_key': 'low_priority',
#     },
#     'high_priority_queue': {
#         'exchange': 'high_priority_queue',
#         'exchange_type': 'direct',
#         'routing_key': 'high_priority',
#     },
# }

app.conf.task_routes = {
    'notifications.tasks.send_notification': {
        'queue': lambda task, *args, **kwargs: (
            high_priority_queue if task.request.kwargs.get('priority_group') == 'high'\
                                  else low_priority_queue
        ),
    }
}

app.config_from_object("django.conf:settings", namespace="CELERY"),
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
