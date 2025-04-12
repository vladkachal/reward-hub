from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from .models import RewardLog, ScheduledReward

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "execute_at"]
    search_fields = ["id", "user__email", "user__username"]
    autocomplete_fields = ["user"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[ScheduledReward]:
        return super().get_queryset(request).select_related("user")

    def has_change_permission(
        self, request: HttpRequest, obj: RewardLog = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: RewardLog = None
    ) -> bool:
        return False


@admin.register(RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "given_at"]
    search_fields = ["id", "user__email", "user__username"]
    autocomplete_fields = ["user"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[RewardLog]:
        return super().get_queryset(request).select_related("user")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: RewardLog = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: RewardLog = None
    ) -> bool:
        return False
