from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

if TYPE_CHECKING:
    from .models import User


class UserQuerySet(models.QuerySet):
    def active(self) -> models.QuerySet[User]:
        return self.filter(is_active=True)


class UserManager(DjangoUserManager.from_queryset(UserQuerySet)):
    pass
