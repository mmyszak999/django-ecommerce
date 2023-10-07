from uuid import UUID

from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from django.shortcuts import get_object_or_404

from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.orders.serializers import (
    CartOutputSerializer,
    CartItemOutputSerializer,
    CartItemInputSerializer,
    CartItemQuantityInputSerializer,
    OrderOutputSerializer,
    OrderInputSerializer,
    CartItemUpdateSerializer
)
from src.apps.orders.services.order_service import *
from src.apps.orders.services.cart_service import CartCreateService, CartItemCreateService, CartItemUpdateService


class CartListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def create(self, request, *args, **kwargs):
        username = request.user.username
        service = CartCreateService()
        cart = service.create_cart(username)
        return Response(
            self.get_serializer(cart).data,
            status=status.HTTP_201_CREATED,
        )


class CartDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer


class CartItemsListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer

    def create(self, request, **kwargs):
        cart_id = self.kwargs.get("pk")
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CartItemCreateService()
        cartitem = service.cart_item_create(
            cart_id=cart_id, data=serializer.validated_data
        )
        return Response(
            self.get_serializer(cartitem).data,
            status=status.HTTP_201_CREATED,
        )


class CartItemsDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer

    def get_object(self):
        id = self.kwargs.get("cart_item_pk")
        cart_id = self.kwargs.get("pk")
        obj = get_object_or_404(CartItem, id=id, cart_id=cart_id)
        return obj
    
    def update(self, request: Request, pk: UUID, cart_item_pk: UUID):
        service = CartItemUpdateService()
        instance = self.get_object()
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_cart_item = service.cart_item_update(
            data=serializer.validated_data, instance=instance
        )
        return Response(
            self.get_serializer(updated_cart_item).data, status=status.HTTP_200_OK
        )


class OrderCreateAPIView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer

    def create(self, request, *args, **kwargs):
        pass


class OrderListAPIView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer


class OrderDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass