from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.base import ContentFile

from src.apps.products.models import (
    Product,
    ProductInventory,
    ProductCategory,
)
from src.apps.products.services.product_category_service import ProductCategoryCreateService, ProductCategoryUpdateService
from src.apps.products.services.product_service import ProductCreateService, ProductUpdateService
from src.apps.products.utils import generate_image_file

User = get_user_model()


class TestCategoryService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_service = ProductCategoryCreateService()
        cls.update_service = ProductCategoryUpdateService()
        
        cls.category_data = {"name": "drinks"}
        cls.update_category_data = {"name": "updated"}
        
    def test_category_service_correctly_creates_category(self):
        category = self.create_service.create_category(request_data=self.category_data)
        category_id = category.id

        self.assertEqual(ProductCategory.objects.all().count(), 1)
        self.assertEqual(ProductCategory.objects.get(id=category_id), category)

    def test_category_service_correctly_updates_category(self):
        category = self.create_service.create_category(self.category_data)
        self.update_service.update_category(request_data=self.update_category_data, instance=category)
        category_id = category.id

        self.assertEqual(ProductCategory.objects.all().count(), 1)



class TestProductService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_service = ProductCreateService()
        cls.update_service = ProductUpdateService()
        
        cls.category = ProductCategory.objects.create(name='fastfood')
        
        image_file = generate_image_file()
        cls.image = ContentFile(image_file.getvalue(), name=image_file.name)
        cls.product_data = {
            "name": "test_product",
            "price": 10.00,
            "description": "test_description",
            "product_image": cls.image,
            "category_id": cls.category.id,
            "inventory": {
                "quantity": 20,
            } 
        }
        cls.updated_product_data = {
            "price": 22.00,
            "inventory": {
                "quantity": 40,
            } 
        }

    def test_product_service_correctly_creates_product(self):
        product = self.create_service.product_create(self.product_data)
        product_id = product.id

        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(ProductCategory.objects.all().count(), 1)
        self.assertEqual(ProductInventory.objects.all().count(), 1)

        self.assertEqual(Product.objects.get(id=product_id), product)


    def test_product_service_correctly_updates_product(self):
        inventory_data = self.updated_product_data["inventory"]
        product = self.create_service.product_create(request_data=self.product_data)
        updated_product = self.update_service.product_update(
            instance=product, request_data=self.updated_product_data
        )

        self.assertEqual(Product.objects.get(id=product.id), updated_product)
        self.assertEqual(
            Product.objects.get(id=updated_product.id).inventory.quantity,
            inventory_data["quantity"],
        )
        self.assertEqual(
            Product.objects.get(id=updated_product.id).price,
            self.updated_product_data['price'],
        )


