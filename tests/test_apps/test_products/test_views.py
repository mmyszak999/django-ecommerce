import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users.models import UserProfile, UserAddress
from src.apps.products.models import (
    Product,
    ProductCategory,
    ProductInventory,
)
from src.apps.products.utils import generate_image_file

User = get_user_model()


class TestProductCategoryViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create(username="customer")
        cls.seller = User.objects.create(username="seller")

        cls.address = UserAddress.objects.create(
            primary_address="address 1/1",
            country="PL",
            city="Warsaw",
            zip_code="00-001",
        )

        cls.customer_profile = UserProfile.objects.create(
            user=cls.customer,
            username=cls.customer.username,
            role='customer',
            email="customer@mail.com",
            phone_number="+48123123123",
        )

        cls.seller_profile = UserProfile.objects.create(
            user=cls.seller,
            username=cls.seller.username,
            role='seller',
            email="seller@mail.com",
            phone_number="+48456456456",
        )

        cls.product_category = ProductCategory.objects.create(name="Food")

        cls.product_category_list_url = reverse("products:category-list")
        cls.product_category_detail_url = reverse(
            "products:category-detail", kwargs={"pk": cls.product_category.id}
        )

    def setUp(self):
        self.client.force_login(user=self.customer)

    def test_user_can_retrieve_product_category(self):
        response = self.client.get(self.product_category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        product_category_data = response.data["results"][0]
        self.assertEqual(product_category_data["name"], self.product_category.name)

    def test_user_can_retrieve_product_category_by_id(self):
        response = self.client.get(self.product_category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(response.json()['id']), self.product_category.id)
        
    def test_user_cannot_delete_product_category(self):
        response = self.client.delete(self.product_category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ProductCategory.objects.exists())

    def test_staff_can_delete_product_category(self):
        self.staff = User.objects.create(username="staff", is_staff=True)
        self.client.force_login(user=self.staff)
        response = self.client.delete(self.product_category_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductCategory.objects.exists())

    def test_anonymous_user_can_retrieve_product_category(self):
        self.client.logout()
        response = self.client.get(self.product_category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        product_category_data = response.data["results"][0]
        self.assertEqual(product_category_data["name"], self.product_category.name)

    def test_anonymous_user_can_retrieve_product_category_by_id(self):
        self.client.logout()
        response = self.client.get(self.product_category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_delete_product_category(self):
        self.client.logout()
        response = self.client.delete(self.product_category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ProductCategory.objects.exists())


class TestProductViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create(username="customer")
        cls.seller = User.objects.create(username="seller")

        cls.address = UserAddress.objects.create(
            primary_address="address 1/1",
            country="PL",
            city="Warsaw",
            zip_code="00-001",
        )

        cls.customer_profile = UserProfile.objects.create(
            user=cls.customer,
            username=cls.customer.username,
            role='customer',
            email="customer@mail.com",
            phone_number="+48123123123",
        )

        cls.seller_profile = UserProfile.objects.create(
            user=cls.seller,
            username=cls.seller.username,
            role='seller',
            email="seller@mail.com",
            phone_number="+48456456456",
        )

        cls.product_category = ProductCategory.objects.create(name="Food")
        cls.product_inventory = ProductInventory.objects.create(quantity=100)
        file = generate_image_file()
        cls.image = ContentFile(file.getvalue(), name=file.name)
        cls.product = Product.objects.create(
            name="Water",
            price="1.99",
            description="waterr",
            category=cls.product_category,
            inventory=cls.product_inventory,
            product_image=cls.image
        )

        cls.product_list_url = reverse("products:product-list")
        cls.product_detail_url = reverse(
            "products:product-detail", kwargs={"pk": cls.product.id}
        )

    def setUp(self):
        self.client.force_login(user=self.customer)

    def test_user_can_retrieve_product(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        
        product_data = response.data["results"][0]
        self.assertEqual(product_data["name"], self.product.name)
        self.assertEqual(product_data["price"], self.product.price)

    def test_user_can_retrieve_product_by_id(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_create_product(self):
        response = self.client.post(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_customer_cannot_delete_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.exists())
    
    def test_seller_can_delete_product(self):
        self.client.force_login(user=self.seller)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.exists())
