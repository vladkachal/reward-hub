from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.RewardLogListView.as_view(),
        name="reward-list",
    ),
]
