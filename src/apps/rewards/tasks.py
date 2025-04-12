import logging

from celery import shared_task

from django.utils.translation import gettext_lazy as _

from .models import ScheduledReward

logger = logging.getLogger(__name__)


@shared_task
def process_scheduled_reward_task(reward_id: int) -> None:
    try:
        reward = ScheduledReward.objects.get(id=reward_id)
    except ScheduledReward.DoesNotExist:
        msg = _(
            f"ScheduledReward with ID {reward_id} was not found."
            f" It may have been deleted or never existed."
        )
        logger.exception(msg)
        return

    ScheduledReward.objects.process_reward(reward)
