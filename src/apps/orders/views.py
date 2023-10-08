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
from django.db.models import Sum, Count, F
from django.utils import timezone

from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.orders.serializers import (
    CartOutputSerializer,
    CartItemOutputSerializer,
    CartItemInputSerializer,
    CartItemQuantityInputSerializer,
    OrderOutputSerializer,
    OrderInputSerializer,
    CartItemUpdateSerializer,
    OrderUpdateSerializer,
    MostOrderedProductsOutputSerializer,
)
from src.apps.orders.services.order_service import OrderCreateService
from src.apps.orders.services.cart_service import CartCreateService, CartItemCreateService, CartItemUpdateService
from src.apps.orders.filters import OrderFilter, MostOrderedProductsFilter
from src.core.permissions import CartOwnerOrAdmin, CustomerOrAdmin, NonCustomer


class CartListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer
    permission_classes = [CustomerOrAdmin]
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user__user=user)

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
    permission_classes = [CustomerOrAdmin]
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user__user=user)


class CartItemsListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemOutputSerializer
    permission_classes = [CartOwnerOrAdmin, CustomerOrAdmin]
    
    def get_queryset(self):
        cart_pk = self.kwargs.get("pk")
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(cart_id=cart_pk, cart__user__user=user)

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
    permission_classes = [CartOwnerOrAdmin, CustomerOrAdmin]

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
    permission_classes = [CustomerOrAdmin]

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
    permission_classes = [CustomerOrAdmin]
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user__user=user)


class OrderDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer
    permission_classes = [CustomerOrAdmin]
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user__user=user)

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

    
class MostOrderedProductsListAPIView(GenericViewSet, ListModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = MostOrderedProductsOutputSerializer
    permission_classes = [NonCustomer]
    
    def get_queryset(self):
        return OrderItem.objects.select_related('product', 'order').values(
            'product__name', 'product__id', "order__order_place_date"
            ).annotate(
                order_count=Count('product'), total_quantity=Sum('quantity'),
                product_name=F('product__name'), product_id=F('product__id')
                ).order_by('-order_count')
    
    def list(self, request: Request, *args, **kwargs):
        max_products = self.request.query_params.get('max_products', len(self.get_queryset()))
        date_from = self.request.query_params.get('date_from', timezone.now() - timezone.timedelta(days=30))
        date_to = self.request.query_params.get('date_to', timezone.now())
        filtered_queryset = self.get_queryset(
            ).filter(order__order_place_date__lte=str(date_to),
                     order__order_place_date__gt=str(date_from))

        page = self.paginate_queryset(filtered_queryset[:int(max_products)])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset[:int(max_products)], many=True)
        return Response(serializer.data)
        