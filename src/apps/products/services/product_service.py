from typing import Any, OrderedDict
from copy import deepcopy
from uuid import UUID

from django.db import transaction

from src.apps.products.models import Product, ProductInventory, ProductCategory
from src.apps.products.serializers import (
    ProductInputSerializer, ProductOutputSerializer,
    ProductInventoryInputSerializer, ProductInventoryOutputSerializer, ProductDataInputSerializer
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
        print(data)

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
    pass
