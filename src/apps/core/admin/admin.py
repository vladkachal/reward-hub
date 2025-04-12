from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.http import HttpRequest


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    autocomplete_fields = ["user"]
    list_filter = ["action_time", "action_flag", "object_repr"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: LogEntry | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: LogEntry | None = None
    ) -> bool:
        return False
