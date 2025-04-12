from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = "apps.auth"
    label = "user_auth"
    verbose_name = _("Authentication & Authorization")
