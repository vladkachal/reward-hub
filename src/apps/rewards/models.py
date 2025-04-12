from __future__ import annotations

import logging

from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models.mixins import UUIDPrimaryKeyModelMixin

from .managers import RewardLogManager, ScheduledRewardManager

logger = logging.getLogger(__name__)

User = get_user_model()


class ScheduledReward(UUIDPrimaryKeyModelMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scheduled_rewards",
        verbose_name=_("user"),
    )
    amount = models.PositiveIntegerField(_("amount"))
    execute_at = models.DateTimeField(_("execute at"))

    objects = ScheduledRewardManager()

    class Meta:
        verbose_name = _("scheduled reward")
        verbose_name_plural = _("scheduled rewards")
        ordering = ["-execute_at"]

    def __str__(self) -> str:
        return f"...{self.short_id}, {self.user}, +{self.amount}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        is_adding = self._state.adding
        super().save(*args, **kwargs)
        if is_adding:
            ScheduledReward.objects.schedule_reward_task(self)
        else:
            msg = _(
                "Updating the 'execute_at' field of a ScheduledReward instance"
                " is not implemented. The execution time of the existing task"
                " remains unchanged."
            )
            logger.warning(msg)


class RewardLog(UUIDPrimaryKeyModelMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reward_logs",
        verbose_name=_("user"),
    )
    amount = models.PositiveIntegerField(_("amount"))
    given_at = models.DateTimeField(_("given at"), auto_now_add=True)

    objects = RewardLogManager()

    class Meta:
        verbose_name = _("reward log")
        verbose_name_plural = _("reward logs")
        ordering = ["-given_at"]

    def __str__(self) -> str:
        return f"...{self.short_id}, {self.user}, +{self.amount}"
