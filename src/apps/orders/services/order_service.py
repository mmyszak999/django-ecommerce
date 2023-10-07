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
    OrderOutputSerializer,
    OrderInputSerializer 
)
from src.apps.orders.entities.cart_entities import (
    CartItemEntity, CartItemUpdateEntity
)
from src.apps.orders.entities.order_entities import (
    OrderEntity, OrderUpdateEntity, OrderItemEntity, OrderItemUpdateEntity
)
from src.apps.orders.validators import validate_item_quantity