import os

from typing import Any

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)


app = Celery("reward-hub")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
