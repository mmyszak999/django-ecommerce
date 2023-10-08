import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from src.apps.users.models import UserProfile, UserAddress
from src.apps.products.models import Product
from src.apps.orders.utils import payment_deadline_calc


User = get_user_model()


class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="cart")

    def __str__(self) -> str:
        return f"Cart {self.pk} | user {self.user.username}. Total: ${self.total}"
    
    @property
    def total(self):
        cartitems = self.cart_items.all()
        return sum(item.total_item_price for item in cartitems)


class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")

    def __str__(self) -> str:
        return f"Item of cart number {self.cart.pk}. Quantity: {self.quantity}"
    
    @property
    def total_item_price(self) -> float:
        return round(self.quantity * self.product.price, 2)
    
    
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_accepted = models.BooleanField(default=False)
    order_place_date = models.DateTimeField(auto_now_add=True)
    payment_deadline = models.DateTimeField(default=payment_deadline_calc)
    
    @property
    def total(self):
        orderitems = self.order_items.all()
        return sum(item.total_item_price for item in orderitems)


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    
    def __str__(self) -> str:
        return f"Order item ({self.product.name}) number {self.order.pk}. Quantity: {self.quantity}"
    
    
    @property
    def total_item_price(self) -> float:
        return self.quantity * self.product.price
