from datetime import timedelta
from typing import Any

from rest_framework import serializers

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import RewardLog, ScheduledReward


class BaseScheduledRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReward
        read_only_fields = ["amount", "execute_at"]


class ScheduledRewardReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReward
        fields = ["id", "amount", "execute_at"]


class ScheduledRewardRequestSerializer(serializers.Serializer):
    def validate(self, attrs: dict) -> dict:
        user = self.context["request"].user
        last_request = ScheduledReward.objects.get_last_manual_request(user)
        if last_request:
            last_request_date = last_request.execute_at.date()
            current_date = timezone.now().date()
            if last_request_date == current_date:
                raise serializers.ValidationError(
                    _("You can only request a reward once per day."),
                    code="reward_already_requested",
                )
        return attrs

    def create(self, validated_data: dict) -> ScheduledReward:
        user = self.context["request"].user
        return ScheduledReward.objects.request_reward(user)

    def to_representation(self, instance: ScheduledReward) -> dict[str, Any]:
        return ScheduledRewardReadSerializer(
            instance, context=self.context
        ).data


class BaseRewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardLog
        read_only_fields = ["amount", "given_at"]


class RewardLogReadSerializer(BaseRewardLogSerializer):
    class Meta(BaseRewardLogSerializer.Meta):
        fields = ["amount", "given_at"]
