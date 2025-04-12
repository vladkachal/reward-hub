import uuid

from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UUIDPrimaryKeyModelMixin(models.Model):
    """
    Abstract model providing a UUID primary key field.
    """

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Auto-generated unique identifier (UUID4)",
    )

    class Meta:
        abstract = True

    @property
    def short_id(self) -> str:
        """
        Returns the last 9 characters of the UUID for display purposes.

        Useful for:
        - Admin interface displays
        - User-facing references

        Note:
        - Not guaranteed to be unique (use full id for database operations)

        Returns:
            str: Last 9 characters of the UUID in lowercase
        """
        return str(self.id)[-9:]


class TimestampModelMixin(models.Model):
    """
    A mixin that adds created_at and updated_at fields.

    The fields avoid using auto_now_add and auto_now attributes to allow
    setting the same value for both created_at and updated_at fields
    when creating an instance.
    """

    created_at = models.DateTimeField(_("created at"), editable=False)
    updated_at = models.DateTimeField(_("updated at"), editable=False)

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self._state.adding:
            self.set_timestamp_fields()
        else:
            self.set_updated_at_field()
        super().save(*args, **kwargs)

    def set_timestamp_fields(self) -> None:
        """
        NOTE: This method must be called manually for each instance
        in instance list before passing it to the **bulk_create** method.
        """

        dt = timezone.now()
        self.created_at = dt
        self.updated_at = dt

    def set_updated_at_field(self) -> None:
        """
        NOTE: This method must be called manually for each instance
        in instance list before passing it to the **bulk_update** method
        or when QuerySet.update() is used.
        """

        dt = timezone.now()
        self.updated_at = dt
