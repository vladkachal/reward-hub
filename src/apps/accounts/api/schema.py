from drf_spectacular.utils import extend_schema, extend_schema_view

from django.utils.translation import gettext_lazy as _

from .serializers import (
    UserProfileReadSerializer,
    UserProfileWriteSerializer,
)


class UserProfileViewSetSchema:
    schema_view = extend_schema_view(
        retrieve=extend_schema(
            summary=_("Retrieve the authenticated user's profile"),
            description=_(
                "This endpoint allows an authenticated user to retrieve"
                " their profile information."
            ),
            responses={"200": UserProfileReadSerializer},
        ),
        partial_update=extend_schema(
            summary=_("Partially update the authenticated user's profile"),
            description=_(
                "This endpoint allows an authenticated user to update specific"
                " fields in their profile.\n\n"
                " Permissions:\n"
                " - only accessible to authenticated users;\n"
                " - users can update only their own profile;\n"
                " - sensitive fields (e.g., permissions, admin status)"
                "  cannot be updated via this endpoint."
            ),
            request=UserProfileWriteSerializer,
            responses={"200": UserProfileReadSerializer},
        ),
    )
