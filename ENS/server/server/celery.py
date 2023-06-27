from __future__ import absolute_import

import os

from celery import Celery
from server.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.development")

app = Celery("server")

app.config_from_object("server.settings.development", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
