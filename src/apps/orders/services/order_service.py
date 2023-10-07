from typing import Any, OrderedDict
from uuid import UUID

from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from src.apps.users.models import UserAddress, UserProfile
from src.apps.products.models import Product
from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.orders.serializers import (
    OrderOutputSerializer,
    OrderInputSerializer,
    OrderItemOutputSerializer
)
from src.apps.orders.entities.order_entities import (
    OrderItemEntity, OrderItemUpdateEntity
)
from src.apps.orders.entities.order_entities import (
    OrderEntity, OrderUpdateEntity, OrderItemEntity, OrderItemUpdateEntity
)
from src.apps.orders.validators import validate_item_quantity


User = get_user_model()

class OrderCreateService:
    def _create_order_items(self, instance: Order, cart_items: list[CartItem]) -> None:
        if cart_items:
            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity
                max_quantity = product.inventory.quantity

                validate_item_quantity(typed_quantity=quantity, max_quantity=max_quantity)
                
                OrderItem.objects.create(product=product, quantity=quantity, order=instance)
                product_inventory = product.inventory
                product_inventory.quantity -= quantity
                product_inventory.save()
    
    @transaction.atomic
    def create_order(cls, cart_id: int, user: User, data: OrderedDict) -> Order:
        cart = get_object_or_404(Cart, id=cart_id)
        cart_items = cart.cart_items.select_related(
            "product", "product__inventory"
        ).all()
        
        address_id = data["address_id"]
        address = get_object_or_404(UserAddress, id=address_id)
        user_profile = UserProfile.objects.get(username=user.username)

        order = Order.objects.create(user=user_profile, address=address)
        cls._create_order_items(instance=order, cart_items=cart_items)
        order.accepted = True
        order.save()

        return order
    

class OrderUpdateService:
    @transaction.atomic
    def update_order(self, instance: Order, user: User, data: OrderedDict) -> Order:
        address_id = data.get("address_id", instance.address.id)
        print(address_id, "ww")
        instance.address = get_object_or_404(UserAddress, id=address_id)
        instance.save()
        return instance


class OrderDestroyService:
    @transaction.atomic
    def destroy_order(self, instance: Order) -> None:
        order_items = instance.order_items.select_related(
            "product", "product__inventory"
        ).all()
        for orderitem in order_items:
            product_inventory = orderitem.product.inventory
            product_inventory.quantity += orderitem.quantity
            product_inventory.save()
        instance.delete()
    