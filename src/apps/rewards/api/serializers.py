from rest_framework import serializers

from ..models import RewardLog


class BaseRewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardLog
        read_only_fields = ["amount", "given_at"]


class RewardLogReadSerializer(BaseRewardLogSerializer):
    class Meta(BaseRewardLogSerializer.Meta):
        fields = ["amount", "given_at"]
