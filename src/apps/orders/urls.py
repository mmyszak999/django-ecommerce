from django.urls import path
from src.apps.orders.views import (
    CartItemsDetailAPIView,
    CartItemsListCreateAPIView,
    CartListCreateAPIView,
    CartDetailAPIView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    OrderListAPIView,
)

app_name = "orders"

urlpatterns = [
    path("carts/", CartListCreateAPIView.as_view({'get': 'list', 'post': 'create'}), name="cart-list"),
    path("carts/<uuid:pk>/", CartDetailAPIView.as_view({"delete": "destroy", 'get': 'retrieve'}), name="cart-detail"),
    path(
        "carts/<uuid:pk>/items/",
        CartItemsListCreateAPIView.as_view({'get': 'list', 'post': 'create'}),
        name="cart-item-list",
    ),
    path(
        "carts/<uuid:pk>/items/<uuid:cart_item_pk>/",
        CartItemsDetailAPIView.as_view({'put': 'update', "delete": "destroy", 'get': 'retrieve'}),
        name="cart-item-detail",
    ),
    path("carts/<uuid:pk>/order/", OrderCreateAPIView.as_view({'post': 'create'}), name="create-order"),
    path("orders/", OrderListAPIView.as_view({'get': 'list'}), name="order-list"),
    path("orders/<uuid:pk>/", OrderDetailAPIView.as_view(
        {'put': 'update', "delete": "destroy", 'get': 'retrieve'}), name="order-detail"),
]