from django.urls import path

from src.apps.users.views import (
    UserRegisterAPIView,
    UserProfileListAPIView,
    UserProfileDetailAPIView
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view({'post': 'create'}), name="register"),
    path("", UserProfileListAPIView.as_view({'get': 'list'}), name="user-profile-list"),
    path(
        "<uuid:pk>/",
        UserProfileDetailAPIView.as_view({'put': 'update', 'get': 'retrieve'}),
        name="user-profile-detail",
    )
]