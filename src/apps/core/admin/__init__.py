from django.contrib import admin as django_admin

from .admin import *  # noqa
from .sites import CustomAdminSite

django_admin.site.__class__ = CustomAdminSite
