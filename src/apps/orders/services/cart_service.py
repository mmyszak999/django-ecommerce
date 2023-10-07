from typing import Any, OrderedDict
from uuid import UUID

from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from src.apps.users.models import UserAddress, UserProfile
from src.apps.products.models import Product
from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.orders.serializers import (
    CartOutputSerializer,
    CartItemOutputSerializer,
    CartItemInputSerializer,
    CartItemQuantityInputSerializer,
    CartItemUpdateSerializer,
    CartItemQuantityUpdateSerializer
)
from src.apps.orders.entities.cart_entities import (
    CartItemEntity, CartItemUpdateEntity
)
from src.apps.orders.entities.order_entities import (
    OrderEntity, OrderUpdateEntity, OrderItemEntity, OrderItemUpdateEntity
)
from src.apps.orders.validators import validate_item_quantity


class CartCreateService:
    def create_cart(self, username: str):
        user = UserProfile.objects.get(username=username)
        return Cart.objects.create(user=user)
    

class CartItemCreateService:
    def _cart_item_create(self, dto: CartItemEntity, product: Product, cart: Cart) -> CartItem:
        return CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=dto.quantity
        )
    
    @classmethod
    def _build_cart_item_dto_from_request_data(cls, request_data: OrderedDict) -> CartItemEntity:
        serializer = CartItemQuantityInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return CartItemEntity(*data.values())
    
    @transaction.atomic
    def cart_item_create(self, cart_id: int, data: OrderedDict) -> CartItem:
        product_id = data.pop("product_id")
        quantity = data.pop("quantity")

        product = get_object_or_404(Product, id=product_id)
        
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            max_quantity = product.inventory.quantity - cartitem.quantity
            
            validate_item_quantity(quantity['quantity'], max_quantity)
            cartitem.quantity += quantity['quantity']
            cartitem.save()
            
        except CartItem.DoesNotExist:
            validate_item_quantity(quantity['quantity'], product.inventory.quantity)
            
            cart = get_object_or_404(Cart, id=cart_id)
            cart_item_dto = self._build_cart_item_dto_from_request_data(quantity)
            cartitem = self._cart_item_create(cart_item_dto, product, cart)
            cartitem.save()
            print("ww")
            
        return cartitem


class CartItemUpdateService:
    def _cart_item_update(self, dto: CartItemUpdateEntity, instance: CartItem) -> CartItem:
        instance.quantity = dto.quantity
        instance.save()
        
        return instance
    
    @classmethod
    def _build_cart_item_dto_from_request_data(cls, request_data: OrderedDict, instance: CartItem) -> CartItemUpdateEntity:
        serializer = CartItemQuantityUpdateSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        return CartItemEntity(
            data.get("quantity", instance.quantity)
            )
    
    @transaction.atomic
    def cart_item_update(self, data: OrderedDict, instance: CartItem) -> CartItem:
        quantity = data.pop('quantity')
        max_quantity = instance.product.inventory.quantity
        validate_item_quantity(quantity['quantity'], max_quantity-instance.quantity)
        
        cart_item_dto = self._build_cart_item_dto_from_request_data(quantity, instance)
        return self._cart_item_update(cart_item_dto, instance)
        