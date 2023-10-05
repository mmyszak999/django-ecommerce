from django.urls import path

from src.apps.users.views import (
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileDetailAPIView
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("", UserProfileListAPIView.as_view(), name="user-profile-list"),
    path(
        "<uuid:pk>/",
        UserProfileDetailAPIView.as_view(),
        name="user-profile-detail",
    )
]