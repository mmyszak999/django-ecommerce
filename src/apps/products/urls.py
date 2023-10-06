from django.urls import path

from src.apps.products.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    ProductCategoryDetailAPIView,
    ProductCategoryListCreateAPIView
)

app_name = "products"

urlpatterns = [
    path("", ProductListCreateAPIView.as_view({'get': 'list', 'post': 'create'}), name="product-list"),
    path("<uuid:pk>/", ProductDetailAPIView.as_view({'put': 'update', "delete": "destroy", 'get': 'retrieve'}), name="product-detail"),
    path("categories/", ProductCategoryListCreateAPIView.as_view({'get': 'list', 'post': 'create'}), name="category-list"),
    path(
        "categories/<uuid:pk>/",
        ProductCategoryDetailAPIView.as_view({'put': 'update', "delete": "destroy", 'get': 'retrieve'}),
        name="category-detail",
    )
]