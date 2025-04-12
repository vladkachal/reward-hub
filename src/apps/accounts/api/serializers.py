from typing import Any

from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()


class UserPermissionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "codename"]


class UserGroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class BaseUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = [
            "id",
            "email",
            "password",
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active",
            "last_login",
            "date_joined",
        ]


class UserProfileReadSerializer(BaseUserProfileSerializer):
    class Meta(BaseUserProfileSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "coins",
        ]


class UserProfileWriteSerializer(BaseUserProfileSerializer):
    class Meta(BaseUserProfileSerializer.Meta):
        fields = [
            "username",
        ]
        extra_kwargs = {
            "username": {"allow_blank": False},
            "first_name": {"allow_blank": False},
            "last_name": {"allow_blank": False},
        }

    def to_representation(self, instance: User) -> dict[str, Any]:
        return UserProfileReadSerializer(instance, context=self.context).data
