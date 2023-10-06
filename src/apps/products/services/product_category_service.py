from typing import Any, OrderedDict
from copy import deepcopy

from django.db import transaction

from src.apps.products.models import ProductCategory
from src.apps.products.serializers import ProductCategoryInputSerializer, ProductCategoryOutputSerializer

from src.apps.products.entities.product_category_entities import (
    ProductCategoryEntity, ProductCategoryUpdateEntity
)


class ProfileCategoryCreateService:
    def product_category_create(self, dto: ProductCategoryEntity) -> ProductCategory:
        return ProductCategory.objects.create(
            name=dto.name
        )
    
    @classmethod
    def _build_product_category_dto_from_request_data(cls, request_data: OrderedDict) -> ProductCategoryEntity:
        serializer = ProductCategoryInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ProductCategoryEntity(*data.values())
        
    @transaction.atomic
    def create_category(self, request_data: OrderedDict) -> UserProfile:
        category_name = request_data.pop("name")
        
        category_name_check = ProductCategory.objects.filter(name=category_name)
        
        if category_name_check:
            raise ValueNotUniqueException(ProductCategory, "name", category_name)
        
        category_dto = self._build_product_category_dto_from_request_data(category_name)
        return self.product_category_create(category_dto)


class ProfileCategoryUpdateService:
    def product_category_update(self, instance: UserAddress, dto: ProductCategoryEntity) -> ProductCategory:
        instance.name = dto.name
        instance.save()
        return instance
    
    @classmethod
    def _build_product_category_dto_from_request_data(cls, instance: ProductCategory, request_data: OrderedDict) -> ProductCategoryUpdateEntity:
        serializer = ProductCategoryInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        return ProductCategoryUpdateEntity(
            name=data.get("name", instance.name)
        )
        
    @transaction.atomic
    def update_category(self, request_data: OrderedDict, instance: ProductCategory) -> ProductCategory:
        category_name = request_data.pop("name")
        
        category_name_check = ProductCategory.objects.filter(name=category_name)
        
        if category_name_check:
            raise ValueNotUniqueException(ProductCategory, "name", category_name)
        
        category_dto = self._build_product_category_dto_from_request_data(instance, category_name)
        return self.product_category_update(instance, category_dto)