from __future__ import annotations

import logging

from datetime import timedelta
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Case, Value, When
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import RewardLog, ScheduledReward

User = get_user_model()

logger = logging.getLogger(__name__)


class ScheduledRewardQuerySet(models.QuerySet):
    def annotate_is_requested_by_user(self) -> models.QuerySet:
        return self.annotate(
            is_requested_by_user=Case(
                When(requested_by_user__isnull=False, then=Value(True)),  # noqa: FBT003
                default=Value(False),  # noqa: FBT003
                output_field=models.BooleanField(),
            )
        )


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

    def request_reward(
        self, user: User, *, amount: int = 10, delay: int = 5
    ) -> ScheduledReward | None:
        """
        Creates a ScheduledReward as a result of a manual reward request
        by the user.
        This method is used when a user explicitly requests a reward.

        Args:
            user (User): The user requesting the reward
            amount (int): The amount of coins to be rewarded
            delay (int): The delay in minutes before the reward is given

        Return:
            The created ScheduledReward object.
        """

        from .models import RewardRequestByUser

        reward = self.create(
            user=user,
            amount=amount,
            execute_at=timezone.now() + timedelta(minutes=delay),
        )

        RewardRequestByUser.objects.create(reward=reward)
        return reward

    def get_last_manual_request(self, user: User) -> ScheduledReward | None:
        """
        Returns the most recent manually requested reward for the given user.

        Args:
            user (User): The user for whom the last reward is requested.

        Return:
            ScheduledReward | None: The latest manually requested reward
            for the user, or None if no such reward exists.
        """

        return (
            self.filter(user=user, requested_by_user__isnull=False)
            .order_by("-execute_at")
            .first()
        )


ScheduledRewardManager = ScheduledRewardManager.from_queryset(
    ScheduledRewardQuerySet
)


class RewardLogQuerySet(models.QuerySet):
    def get_user_rewards(self, user: User) -> models.QuerySet[RewardLog]:
        return self.filter(user=user).order_by("-given_at")


class RewardLogManager(models.Manager): ...


RewardLogManager = RewardLogManager.from_queryset(RewardLogQuerySet)
