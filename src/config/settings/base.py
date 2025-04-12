"""
This file contains the base settings for a project. It provides a foundational
configuration for building other settings files (e.g., development, production).

To use this file, create a new settings file and import this one as the base.
Then, you can override any of the settings in this file or add a new settings
as needed for a project.
"""

from pathlib import Path

from decouple import Csv, config

from django.utils.translation import gettext_lazy as _

from utils import BoolOrDictHandler

CURRENT_ENVIRONMENT = config("CURRENT_ENVIRONMENT")


class CurrentEnv:
    is_dev = CURRENT_ENVIRONMENT == "development"
    is_prod = CURRENT_ENVIRONMENT == "production"
    is_stage = CURRENT_ENVIRONMENT == "staging"
    is_test = CURRENT_ENVIRONMENT == "testing"


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------------------------
# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
admins_csv = Csv(cast=lambda s: tuple(s.split(",")), delimiter=";")
ADMINS = config("ADMINS", cast=admins_csv, default=None)
SITE_ID = 1
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # --------------------------------------------------------------------------
    # Third-party apps
    # API
    "corsheaders",
    "drf_spectacular",
    # --------------------------------------------------------------------------
    # Local apps
    "apps.accounts",
    "apps.auth",
    "apps.core",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# ------------------------------------------------------------------------------
# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = config("ROOT_URLCONF", default="config.urls")
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "TEST": {
            "NAME": f"{config('DATABASE_NAME')}_test",
        },
        "CONN_MAX_AGE": 0,
        "OPTIONS": {
            "pool": config(
                "DATABASE_POOL", cast=BoolOrDictHandler(), default=True
            ),
        },
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [str(BASE_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------------
# MEDIA
# ------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
USE_TZ = True
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
USE_I18N = True
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# ------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_USER_MODEL = "accounts.User"

# ------------------------------------------------------------------------------
# DJANGO-ALLAUTH
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = config(
    "ACCOUNT_ALLOW_REGISTRATION", cast=bool, default=True
)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 10
ACCOUNT_LOGIN_BY_CODE_ENABLED = config(
    "ACCOUNT_LOGIN_BY_CODE_ENABLED", cast=bool, default=True
)
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_ADAPTER = "apps.accounts.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "apps.accounts.adapters.SocialAccountAdapter"
HEADLESS_ONLY = True

# ------------------------------------------------------------------------------
# PASSWORD
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
DJANGO_VALIDATORS_PATH = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.UserAttributeSimilarityValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.MinimumLengthValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.CommonPasswordValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# REDIS
# ------------------------------------------------------------------------------
REDIS_DB_ID_BASE = 0
REDIS_DB_ID_CACHE = 1
REDIS_URL_BASE = config("REDIS_URL_BASE", default="redis://localhost:6379")
REDIS_URL = f"{REDIS_URL_BASE}/{REDIS_DB_ID_BASE}"
REDIS_SSL = REDIS_URL.startswith("rediss://")

# ------------------------------------------------------------------------------
# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL_BASE}/{REDIS_DB_ID_CACHE}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

# ------------------------------------------------------------------------------
# COMPONENTS
# ------------------------------------------------------------------------------
from .components.api import *  # noqa
from .components.celery import *  # noqa
from .components.logging_ import *  # noqa
