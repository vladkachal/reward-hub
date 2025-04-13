from drf_spectacular.utils import extend_schema, extend_schema_view

from django.utils.translation import gettext_lazy as _

from .serializers import ScheduledRewardReadSerializer

schedule_reward_request_schema_view = extend_schema_view(
    post=extend_schema(
        summary=_("Request a reward"),
        description=_(
            "Endpoint for users to request a reward.\n\n"
            " - The user can only request a reward once per day.\n"
            " - The reward amount is fixed at 10 coins.\n"
            " - Upon a successful request, a ScheduledReward is created which"
            "  will be processed after 5 minutes."
        ),
        responses={
            201: ScheduledRewardReadSerializer,
        },
    ),
)

reward_log_schema_view = extend_schema_view(
    get=extend_schema(
        summary=_("List all rewards for the authenticated user"),
        description=_(
            "Retrieve a list of all rewards associated with the authenticated"
            " user."
        ),
    ),
)
