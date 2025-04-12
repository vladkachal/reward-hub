from drf_spectacular.utils import extend_schema, extend_schema_view

from django.utils.translation import gettext_lazy as _

reward_log_schema_view = extend_schema_view(
    get=extend_schema(
        summary=_("List all rewards for the authenticated user"),
        description=_(
            "Retrieve a list of all rewards associated with the authenticated"
            " user."
        ),
    ),
)
