from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RewardConfig(AppConfig):
    name = "apps.rewards"
    verbose_name = _("Rewards")
