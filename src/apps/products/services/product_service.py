from typing import Any, OrderedDict
from copy import deepcopy
from uuid import UUID

from django.db import transaction

from src.apps.products.models import Product, ProductInventory, ProductCategory
from src.apps.products.serializers import (
    ProductInputSerializer, ProductOutputSerializer,
    ProductInventoryInputSerializer, ProductInventoryOutputSerializer, ProductDataInputSerializer,
    ProductUpdateDataInputSerializer, ProductUpdateInputSerializer, ProductInventoryUpdateInputSerializer
)
from src.apps.products.entities.product_inventory_entities import (
    ProductInventoryEntity, ProductInventoryUpdateEntity
)
from src.apps.products.entities.product_entities import (
    ProductEntity, ProductUpdateEntity
)


class ProductCreateService:
    def product_inventory_create(self, dto: ProductInventoryEntity) -> ProductInventory:
        return ProductInventory.objects.create(
            quantity=dto.quantity
        )
    
    @classmethod
    def _build_product_inventory_dto_from_request_data(cls, request_data: OrderedDict) -> ProductInventoryEntity:
        serializer = ProductInventoryInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ProductInventoryEntity(*data.values())
    
    def _product_create(self, dto: ProductEntity, inventory: ProductInventory, category: ProductCategory) -> Product:
        product = Product.objects.create(
            name=dto.name,
            price=dto.price,
            description=dto.description,
            inventory=inventory,
            category=category,
            product_image=dto.product_image
            )
        
        return product

    @classmethod
    def _build_product_dto_from_request_data(cls, request_data: OrderedDict) -> ProductEntity:
        serializer = ProductDataInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ProductEntity(*data.values())
    
    def product_create(self, request_data: OrderedDict) -> Product:
        inventory_data = request_data['inventory']
        inventory_dto = self._build_product_inventory_dto_from_request_data(inventory_data)
        product_inventory = self.product_inventory_create(inventory_dto)
        
        category_id, _ = request_data.pop('category_id'), request_data.pop('inventory')
        product_category = ProductCategory.objects.get(id=category_id)
        product_dto = self._build_product_dto_from_request_data(request_data)
        
        return self._product_create(product_dto, product_inventory, product_category)
    

class ProductUpdateService:
    def product_inventory_update(self, instance: ProductInventory, dto: ProductInventoryUpdateEntity) -> ProductInventory:
        print("3")
        instance.quantity = dto.quantity
        instance.save()
        return instance
    
    @classmethod
    def _build_product_inventory_dto_from_request_data(
        cls, instance: ProductInventory, request_data: OrderedDict) -> ProductInventoryUpdateEntity:
        print("1")
        print(request_data, "prod")
        serializer = ProductInventoryUpdateInputSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        print("2")
        return ProductInventoryUpdateEntity(
            quantity=data.get("quantity", instance.quantity)
        )
    
    def _product_update(
        self, dto: ProductUpdateEntity, inventory: ProductInventory,
        category: ProductCategory, instance: Product) -> Product:
        print("6")
        instance.name = dto.name
        instance.price = dto.price
        instance.description = dto.description
        instance.product_image = dto.product_image
        instance.save()
        
        return instance

    @classmethod
    def _build_product_dto_from_request_data(cls, instance: Product, request_data: OrderedDict) -> ProductUpdateEntity:
        print("4")
        serializer = ProductUpdateDataInputSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        print("5")

        return ProductUpdateEntity(
            name=data.get("name", instance.name),
            price=data.get("price", instance.price),
            description=data.get("description", instance.description),
            product_image=data.get("product_image", instance.product_image)
        )
    
    @transaction.atomic
    def product_update(self, request_data: OrderedDict, instance: Product) -> Product:
        print(request_data, "wd")
        inventory_data = request_data.get('inventory')
        inventory_dto = self._build_product_inventory_dto_from_request_data(instance.inventory, inventory_data)
        product_inventory = self.product_inventory_update(instance.inventory, inventory_dto)
        
        category_id, _ = request_data.pop('category_id'), request_data.pop('inventory')
        product_category = ProductCategory.objects.get(id=category_id)
        product_dto = self._build_product_dto_from_request_data(request_data)
        
        return self._product_update(product_dto, product_inventory, product_category, instance)
