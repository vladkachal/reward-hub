from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models.mixins import UUIDPrimaryKeyModelMixin

from .managers import UserManager
from .validators import MinLengthUsernameValidator, UnicodeUsernameValidator


class Group(DjangoGroup):
    class Meta:
        proxy = True


class User(UUIDPrimaryKeyModelMixin, AbstractUser):
    username_validator = UnicodeUsernameValidator()

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        validators=[
            username_validator,
            MinLengthUsernameValidator(limit_value=3),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and _ only."
        ),
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    coins = models.IntegerField(_("coins"), default=0, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects: ClassVar[UserManager] = UserManager()

    class Meta(AbstractUser.Meta):  # type: ignore[name-defined]
        pass

    def __str__(self) -> str:
        return self.email
