from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.base import ContentFile

from src.apps.products.models import Product, ProductInventory, ProductCategory
from src.apps.orders.models import Cart, CartItem, Order, OrderItem
from src.apps.users.models import UserAddress, UserProfile
from src.apps.products.utils import generate_image_file

User = get_user_model()


class TestCartViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer1 = User.objects.create(username="customer1")
        cls.customer2 = User.objects.create(username="customer2")
        cls.seller = User.objects.create(username="seller")

        cls.address = UserAddress.objects.create(
            primary_address="address 1/1",
            country="PL",
            city="Warsaw",
            zip_code="00-001",
        )

        cls.customer1_profile = UserProfile.objects.create(
            user=cls.customer1,
            username=cls.customer1.username,
            role='customer',
            email="customer1@mail.com",
            phone_number="+48123123123",
        )
        
        cls.customer2_profile = UserProfile.objects.create(
            user=cls.customer2,
            username=cls.customer2.username,
            role='customer',
            email="customer2@mail.com",
            phone_number="+48123123678",
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
        image_file = generate_image_file()
        cls.image = ContentFile(image_file.getvalue(), name=image_file.name)
        cls.product = Product.objects.create(
            name="Water",
            price="1.99",
            description="waterr",
            category=cls.product_category,
            inventory=cls.product_inventory,
            product_image=cls.image
        )
        cls.cart = Cart.objects.create(user=cls.customer1_profile)
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart, product=cls.product, quantity=10
        )
        cls.cart_list_url = reverse("orders:cart-list")
        cls.cart_detail_url = reverse("orders:cart-detail", kwargs={"pk": cls.cart.id})

    def setUp(self):
        self.client.force_login(user=self.customer1)

    def test_customer_can_retrieve_cart(self):
        response = self.client.get(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(uuid.UUID(response.data["results"][0]["id"]), self.cart.id)

    def test_user_can_retrieve_cart_by_id(self):
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_delete_cart(self):
        response = self.client.delete(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_retrieve_other_users_cart(self):
        self.client.force_login(user=self.customer2)
        response = self.client.get(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 0)

    def test_other_user_cannot_retrieve_other_users_cart_by_id(self):
        self.client.force_login(user=self.customer2)
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_cannot_delete_other_users_cart(self):
        self.client.force_login(user=self.customer2)
        response = self.client.delete(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Cart.objects.exists())
