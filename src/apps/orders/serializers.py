from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.users.serializers import UserAddressOutputSerializer, UserOrderOutputSerializer


class CartItemQuantityInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, validators=[MinValueValidator(0)])


class CartItemQuantityUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, validators=[MinValueValidator(0)], required=False)
    

class CartItemInputSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = CartItemQuantityInputSerializer()


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = CartItemQuantityUpdateSerializer()
    
    
class CartItemOutputSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_id",
            "product_name",
            "quantity",
            "total_item_price"
        )
        read_only_fields = fields


class CartOutputSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    cart_items = CartItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "username",
            "cart_items",
            "total",
        )
        read_only_fields = fields


class OrderInputSerializer(serializers.Serializer):
    address_id = serializers.CharField()


class OrderUpdateSerializer(serializers.Serializer):
    address_id = serializers.CharField(required=False)


class OrderItemOutputSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_id",
            "product_name",
            "quantity",
            "total_item_price"
        )
        read_only_fields = fields


class OrderOutputSerializer(serializers.ModelSerializer):
    userprofile = UserOrderOutputSerializer(
        source="user.userprofile", many=False, read_only=True
    )
    address = UserAddressOutputSerializer(many=False, read_only=True)
    order_items = OrderItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "userprofile",
            "address",
            "total",
            "address",
            "order_accepted",
            "order_items",
            "order_place_date",
            "payment_deadline"
        )
        read_only_fields = fields


class MostOrderedProductsOutputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    product_name = serializers.CharField()
    order_count = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    