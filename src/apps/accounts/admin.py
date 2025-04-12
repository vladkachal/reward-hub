from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import (
    GroupAdmin as DjangoGroupAdmin,
    UserAdmin as DjangoUserAdmin,
)
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _

from .models import Group, User

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    ]
    readonly_fields = ["id"]
    fieldsets = [
        (None, {"fields": ("username", "email", "password", "id")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    ]
    ordering = ["-date_joined"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        return super().get_queryset(request).all()
