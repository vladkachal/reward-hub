from rest_framework.generics import CreateAPIView, ListAPIView

from django.db.models import QuerySet

from ..models import RewardLog
from .schema import reward_log_schema_view, schedule_reward_request_schema_view
from .serializers import (
    RewardLogReadSerializer,
    ScheduledRewardRequestSerializer,
)


@schedule_reward_request_schema_view
class ScheduledRewardRequestView(CreateAPIView):
    serializer_class = ScheduledRewardRequestSerializer


@reward_log_schema_view
class RewardLogListView(ListAPIView):
    serializer_class = RewardLogReadSerializer

    def get_queryset(self) -> QuerySet[RewardLog]:
        return RewardLog.objects.get_user_rewards(self.request.user)
