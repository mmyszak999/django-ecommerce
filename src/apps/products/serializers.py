from rest_framework import serializers

from src.apps.products.models import Product, ProductCategory, ProductInventory


class ProductCategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductCategoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "name")
        read_only_fields = fields


class ProductInventoryInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(initial=0, allow_null=True)


class ProductInventoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ("id", "quantity", "sold")
        read_only_fields = fields


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField(default=0, allow_null=True)
    description = serializers.CharField(required=False)
    product_image = serializers.ImageField()
    category_id = serializers.UUIDField()
    inventory = ProductInventoryInputSerializer(many=False, required=True)
    

class ProductDataInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField(default=0, allow_null=True)
    description = serializers.CharField(required=False)
    product_image = serializers.ImageField()


class ProductOutputSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "category",
            "product_image",
            "product_thumbnail",
        )
        read_only_fields = fields

class ProductDetailOutputSerializer(serializers.ModelSerializer):
    inventory = ProductInventoryOutputSerializer(many=False, read_only=True)
    category = ProductCategoryOutputSerializer(many=False, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "product_image",
            "product_thumbnail",
            "inventory",
            "category",
        )
        read_only_fields = fields