from rest_framework import routers

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "profile/",
        views.UserProfileViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
    ),
]
