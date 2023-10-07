from django.urls import include, path


urlpatterns = [
    path("users/", include("src.apps.users.urls", namespace="users")),
    path("products/", include("src.apps.products.urls", namespace="products")),
    path("", include("src.apps.orders.urls", namespace="orders")),
]