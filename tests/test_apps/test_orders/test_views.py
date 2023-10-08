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
    
    def test_seller_cannot_retrieve_cart(self):
        self.client.force_login(user=self.seller)
        response = self.client.get(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_anonymous_user_cannot_retrieve_other_cart_by_id(self):
        self.client.logout()
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_cart(self):
        self.client.logout()
        response = self.client.delete(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Cart.objects.exists())


class TestCartItemViews(APITestCase):
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
        
        cls.cart_item_list_url = reverse(
            "orders:cart-item-list", kwargs={"pk": cls.cart.id}
        )
        cls.cart_item_detail_url = reverse(
            "orders:cart-item-detail",
            kwargs={"pk": cls.cart.id, "cart_item_pk": cls.cart_item.id},
        )

        cls.other_cart = Cart.objects.create(user=cls.customer2_profile)
        cls.other_cart_item = CartItem.objects.create(
            cart=cls.other_cart, product=cls.product, quantity=10
        )

        cls.wrong_cart_correct_cart_item_detail_url = reverse(
            "orders:cart-item-detail",
            kwargs={"pk": cls.other_cart.id, "cart_item_pk": cls.cart_item.id},
        )
        cls.correct_cart_wrong_cart_item_detail_url = reverse(
            "orders:cart-item-detail",
            kwargs={"pk": cls.cart.id, "cart_item_pk": cls.other_cart_item.id},
        )

    def setUp(self):
        self.client.force_login(user=self.customer1)

    def test_user_can_retrieve_cart_items(self):
        response = self.client.get(self.cart_item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            uuid.UUID(response.data["results"][0]["id"]), self.cart_item.id
        )

    def test_user_can_retrieve_cart_item_by_id(self):
        response = self.client.get(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_cart_item(self):
        response = self.client.delete(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(cart__user=self.customer1_profile).exists())

    def test_user_cannot_retrieve_cart_item_with_wrong_cart_id(self):
        response = self.client.get(self.wrong_cart_correct_cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_retrieve_cart_item_belonging_to_other_users_cart(self):
        response = self.client.get(self.correct_cart_wrong_cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_seller_cannot_retrieve_other_users_cart_item(self):
        self.client.force_login(user=self.seller)
        response = self.client.get(self.cart_item_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_retrieve_other_users_cart_item(self):
        self.client.force_login(user=self.customer2)
        response = self.client.get(self.cart_item_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_retrieve_other_users_cart_item_by_id(self):
        self.client.force_login(user=self.customer2)
        response = self.client.get(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_delete_other_users_cart_item(self):
        self.client.force_login(user=self.customer2)
        response = self.client.delete(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CartItem.objects.filter(cart__user=self.customer1_profile).exists())

    def test_anonymous_user_cannot_retrieve_cart_item(self):
        self.client.logout()
        response = self.client.get(self.cart_item_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_retrieve_cart_item_by_id(self):
        self.client.logout()
        response = self.client.get(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_cart_item(self):
        self.client.logout()
        response = self.client.delete(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrderViews(APITestCase):
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
        
        cls.order = Order.objects.create(user=cls.customer1_profile)
        cls.order_item = OrderItem.objects.create(
            order=cls.order, product=cls.product, quantity=10
        )

        cls.order_list_url = reverse("orders:order-list")
        cls.order_detail_url = reverse(
            "orders:order-detail", kwargs={"pk": cls.order.id}
        )

    def setUp(self):
        self.client.force_login(user=self.customer1)

    def test_user_can_retrieve_order(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(uuid.UUID(response.data["results"][0]["id"]), self.order.id)
    
    def test_seller_cannot_retrieve_order(self):
        self.client.force_login(user=self.seller)
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_retrieve_order_by_id(self):
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_retrieve_other_users_order_by_id(self):
        self.client.force_login(self.customer2)
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_cannot_retrieve_order(self):
        self.client.logout()
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_retrieve_order_by_id(self):
        self.client.logout()
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_order(self):
        self.client.logout()
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
