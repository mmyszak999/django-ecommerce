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
from django_filters import rest_framework as filters

from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.orders.serializers import (
    CartOutputSerializer,
    CartItemOutputSerializer,
    CartItemInputSerializer,
    CartItemQuantityInputSerializer,
    OrderOutputSerializer,
    OrderInputSerializer,
    CartItemUpdateSerializer,
    OrderUpdateSerializer
)
from src.apps.orders.services.order_service import OrderCreateService, OrderUpdateService, OrderDestroyService
from src.apps.orders.services.cart_service import CartCreateService, CartItemCreateService, CartItemUpdateService
from src.apps.orders.filters import OrderFilter



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

    def create(self, request: Response, pk: UUID):
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
    
    def update(self, request: Request, pk: UUID, cart_item_pk: UUID) -> Response:
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

    def create(self, request: Request, pk: UUID) -> Response:
        service = OrderCreateService()
        cart_id = self.kwargs.get("pk")
        serializer = OrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = service.create_order(
            cart_id=cart_id,
            user=self.request.user,
            data=serializer.validated_data,
        )
        return Response(
            self.get_serializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListAPIView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter


class OrderDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer

    def update(self, request: Request, pk: UUID) -> Response:
        service = OrderUpdateService()
        instance = self.get_object()
        if instance.order_accepted:
            return Response(
                {"order_accepted": "Order already accepted and can't be modified!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_order = service.update_order(
            instance=instance, user=self.request.user, data=serializer.validated_data
        )
        return Response(
            self.get_serializer(updated_order).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, pk: UUID):
        instance = self.get_object()
        service = OrderDestroyService()
        if instance.order_accepted:
            return Response(
                {"order_accepted": "Order already accepted and cant be deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service.destroy_order(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)