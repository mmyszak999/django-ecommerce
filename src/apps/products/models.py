import uuid

from django.db import models

from src.apps.products.utils import resize_thumbnail


class ProductCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class ProductInventory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    quantity = models.IntegerField()
    sold = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self) -> str:
        return f"Available : {self.quantity} | {self.product.name}"


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    description = models.CharField(max_length=1000, blank=True, null=True)

    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    inventory = models.OneToOneField(
        ProductInventory, on_delete=models.CASCADE, related_name="product"
    )
    product_image = models.ImageField()
    product_thumbnail = models.ImageField()
    
    def save(self):
        super().save()
        resize_thumbnail(self.product_image, self.product_thumbnail)
