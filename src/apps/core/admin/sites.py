from typing import Any

from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy


class CustomAdminSite(admin.AdminSite):
    site_title: str = None
    site_header: str = None
    index_title: str = None

    def each_context(self, *args: Any, **kwargs: Any) -> dict:
        self.set_site_metadata()
        return super().each_context(*args, **kwargs)

    def set_site_metadata(self) -> None:
        """
        This approach sets metadata using data from the Site model,
        preventing direct database access during initialization and
        avoiding the associated runtime warning (APPS_NOT_READY_WARNING_MSG).
        NOTE: Overriding the default admin site does not help avoid the warning.
        """

        if not self.site_title:
            site = Site.objects.get_current()
            self.site_title = gettext_lazy(f"{site.name} site admin")
            self.site_header = gettext_lazy(f"{site.name} administration")
            self.index_title = gettext_lazy(
                f"Welcome to {site.name} administration portal"
            )
