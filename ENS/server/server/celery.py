from __future__ import absolute_import

import os

from celery import Celery
from server.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.development")

app = Celery("server")

app.config_from_object("django.conf:settings", namespace="CELERY"),
app.conf.broker_connection_retry_on_startup = True

app.conf.task_queues = {
    'low_priority_queue': {
        'exchange': 'low_priority_queue',
        'exchange_type': 'direct',
        'routing_key': 'low_priority',
    },
    'high_priority_queue': {
        'exchange': 'high_priority_queue',
        'exchange_type': 'direct',
        'routing_key': 'high_priority',
    },
}

app.conf.task_routes = {
    'notifications.tasks.send_notification': {
        'queue': lambda task, *args, **kwargs: (
            'high_priority_queue' if task.request.kwargs.get('priority_group') == 'high'\
                                  else 'low_priority_queue'
        ),
    }
}

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
