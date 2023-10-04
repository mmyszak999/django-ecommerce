from django.urls import include, path


urlpatterns = [
    path("users/", include("src.apps.users.urls", namespace="users")),
]