from rest_framework.generics import ListAPIView

from django.db.models import QuerySet

from ..models import RewardLog
from .schema import reward_log_schema_view
from .serializers import RewardLogReadSerializer


@reward_log_schema_view
class RewardLogListView(ListAPIView):
    serializer_class = RewardLogReadSerializer

    def get_queryset(self) -> QuerySet[RewardLog]:
        return RewardLog.objects.get_user_rewards(self.request.user)
