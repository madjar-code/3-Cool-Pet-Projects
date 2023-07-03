from __future__ import absolute_import

import os

from celery import Celery
from server.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.development")

app = Celery("server")

app.config_from_object("django.conf:settings", namespace="CELERY"),
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
