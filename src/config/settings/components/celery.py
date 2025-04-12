import ssl

from ..base import (
    REDIS_SSL,
    REDIS_URL_BASE,
    TIME_ZONE,
    USE_TZ,
    CurrentEnv,
)

REDIS_DB_ID_CELERY_BROKER = 2
REDIS_DB_ID_CELERY_RESULT_BACKEND = 3

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = f"{REDIS_URL_BASE}/{REDIS_DB_ID_CELERY_BROKER}"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
CELERY_RESULT_BACKEND = f"{REDIS_URL_BASE}/{REDIS_DB_ID_CELERY_RESULT_BACKEND}"
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 6 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 2 * 60
CELERY_RESULT_SERIALIZER = "json"
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

if CurrentEnv.is_dev:
    CELERY_TASK_EAGER_PROPAGATES = True
