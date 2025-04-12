from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.contrib.auth import get_user_model

from .schema import (
    UserProfileViewSetSchema,
)
from .serializers import (
    UserProfileReadSerializer,
    UserProfileWriteSerializer,
)

User = get_user_model()


@UserProfileViewSetSchema.schema_view
class UserProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    schema_tags = ["Accounts"]

    def retrieve(self, request: Request) -> Response:
        serializer = UserProfileReadSerializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request: Request) -> Response:
        serializer = UserProfileWriteSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
