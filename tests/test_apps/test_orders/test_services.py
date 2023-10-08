from django.http.response import Http404
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core import mail
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError

from src.apps.users.models import UserAddress, UserProfile
from src.apps.products.models import Product, ProductInventory, ProductCategory
from src.apps.orders.models import Order, OrderItem, Cart, CartItem
from src.apps.orders.services.cart_service import CartItemCreateService, CartItemUpdateService
from src.apps.orders.services.order_service import OrderCreateService
from src.apps.products.utils import generate_image_file
from src.core.exceptions import MaxQuantityExceededException

User = get_user_model()


class TestCartService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create(username="customer")
        cls.seller = User.objects.create(username="seller")

        cls.create_service = CartItemCreateService()
        cls.update_service = CartItemUpdateService()
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
        cls.cart = Cart.objects.create(user=cls.customer_profile)

        cls.cart_item_data = {
            "product_id": cls.product.id,
            "quantity": {
                "quantity": 10,
            } 
            }
        
        cls.updated_cart_item_data = {
            "quantity": {
                "quantity": 5,
            } 
        }

    def test_cart_service_correctly_creates_cart_item(self):
        cart_item = self.create_service.cart_item_create(
            cart_id=self.cart.id, data=self.cart_item_data
        )

        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(CartItem.objects.get(id=cart_item.id).cart, self.cart)

    def test_cart_service_raises_validation_error_when_stock_is_small(self):
        self.cart_item_data["quantity"]['quantity'] = self.product_inventory.quantity + 1
        with self.assertRaises(MaxQuantityExceededException):
            cart_item = self.create_service.cart_item_create(
                cart_id=self.cart.id, data=self.cart_item_data
            )
        self.assertEqual(CartItem.objects.all().count(), 0)

    def test_cart_service_updates_quantity_instead_of_duplicating_cart_item(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        cart_item = self.create_service.cart_item_create(
            cart_id=self.cart.id, data=self.cart_item_data
        )

        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(CartItem.objects.get(id=cart_item.id), cart_item)
        self.assertEqual(CartItem.objects.get(id=cart_item.id).quantity, 11)

    def test_cart_service_correctly_updates_cart_item(self):
        quantity = self.updated_cart_item_data["quantity"]['quantity']
        cart_item = self.create_service.cart_item_create(
            cart_id=self.cart.id, data=self.cart_item_data
        )
        updated_cart_item = self.update_service.cart_item_update(
            instance=cart_item, data=self.updated_cart_item_data
        )
        self.assertIs(cart_item, updated_cart_item)
        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(
            CartItem.objects.get(id=updated_cart_item.id).quantity, quantity
        )

    def test_cart_service_raises_validation_error_when_stock_is_small_on_update(self):
        quantity = self.cart_item_data["quantity"]["quantity"]
        self.updated_cart_item_data["quantity"]["quantity"] = self.product_inventory.quantity + 1
        cart_item = self.create_service.cart_item_create(
            cart_id=self.cart.id, data=self.cart_item_data
        )
        with self.assertRaises(MaxQuantityExceededException):
            cart_item = self.update_service.cart_item_update(
                instance=cart_item, data=self.updated_cart_item_data
            )
        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(cart_item.quantity, quantity)


class TestOrderService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create(username="customer")
        cls.seller = User.objects.create(username="seller")

        cls.create_service = OrderCreateService()
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
        cls.cart = Cart.objects.create(user=cls.customer_profile)
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart, product=cls.product, quantity=10
        )
        cls.order_data = {
            "address_id": cls.address.id,
        }
    

    def test_order_service_correctly_creates_order_with_no_coupon(self):
        order = self.create_service.create_order(
            self.cart.id, user=self.customer, data=self.order_data
        )

        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Order.objects.get(id=order.id), order)
        self.assertEqual(Cart.objects.all().count(), 0)
        self.assertEqual(CartItem.objects.all().count(), 0)

    
    def test_order_service_sends_email_after_creating_order(self):
        order = self.create_service.create_order(
            self.cart.id, user=self.customer, data=self.order_data
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Confirmation of order #{}".format(order.id))

        self.assertEqual(mail.outbox[0].from_email, "dontreply@djangoecommerce.com")
        self.assertEqual(mail.outbox[0].to, ["{}".format(order.user.email)])

    
    
    def test_order_service_correctly_updates_inventory_of_products(self):
        product_inventory_quantity = self.product.inventory.quantity
        order = self.create_service.create_order(
            self.cart.id, user=self.customer, data=self.order_data
        )
        order_item = OrderItem.objects.filter(order=order).get()

        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(
            order_item.product.inventory.quantity,
            product_inventory_quantity - order_item.quantity,
        )