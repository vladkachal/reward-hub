from django.urls import include, path

app_name = "api"

urlpatterns = [
    path(
        "docs/",
        include("config.api.docs.urls"),
    ),
    path(
        "",
        include("apps.auth.api.urls"),
    ),
    path(
        "accounts/",
        include("apps.accounts.api.urls"),
    ),
]
