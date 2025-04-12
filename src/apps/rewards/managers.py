from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import RewardLog, ScheduledReward

User = get_user_model()

logger = logging.getLogger(__name__)


class ScheduledRewardQuerySet(models.QuerySet): ...


class ScheduledRewardManager(models.Manager):
    @staticmethod
    def schedule_reward_task(reward: ScheduledReward) -> None:
        """
        Schedules a task to process the reward at a specified future time.

        Args:
            reward (ScheduledReward): The scheduled reward instance for
               which the task needs to be scheduled.
        """

        from .tasks import process_scheduled_reward_task

        process_scheduled_reward_task.apply_async(
            args=[reward.id],
            eta=reward.execute_at,
        )

    @transaction.atomic()
    def process_reward(self, reward: ScheduledReward) -> None:
        """
        Processes a scheduled reward by updating the user's coins and creating
        a log entry.

        Args:
            reward (ScheduledReward): The scheduled reward instance
                to be processed.

        Raises:
            DoesNotExist: If the scheduled reward is not found in the database.
        """

        from .models import RewardLog

        if reward.execute_at > timezone.now():
            self.schedule_reward_task(reward)
            msg = _(
                f"ScheduledReward with ID {reward.id} cannot be processed yet"
                f" as 'execute_at' is in the future. A new task has been"
                f" scheduled for {reward.execute_at}."
            )
            logger.warning(msg)
            return

        with transaction.atomic():
            user = User.objects.select_for_update().get(id=reward.user.id)
            user.coins += reward.amount
            user.save()
            RewardLog.objects.create(user=reward.user, amount=reward.amount)


ScheduledRewardManager = ScheduledRewardManager.from_queryset(
    ScheduledRewardQuerySet
)


class RewardLogQuerySet(models.QuerySet):
    def get_user_rewards(self, user: User) -> models.QuerySet[RewardLog]:
        return self.filter(user=user).order_by("-given_at")


class RewardLogManager(models.Manager): ...


RewardLogManager = RewardLogManager.from_queryset(RewardLogQuerySet)
