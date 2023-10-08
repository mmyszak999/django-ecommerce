from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users.models import UserProfile, UserAddress

User = get_user_model()


class TestUserProfileViews(APITestCase):
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
        cls.customer_profile.address.add(cls.address)

        cls.user_profile_list_url = reverse("users:user-profile-list")
        cls.user_profile_detail_url = reverse(
            "users:user-profile-detail",
            kwargs={"pk": cls.customer_profile.id},
        )

    def setUp(self):
        self.client.force_login(user=self.customer)
    
    def test_user_can_retrieve_their_profile(self):
        response = self.client.get(self.user_profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        customer_profile_data = response.data["results"][0]
        self.assertEqual(
            customer_profile_data["phone_number"], self.customer_profile.phone_number
        )
    
    def test_non_staff_user_cannot_get_all_profiles(self):
        response = self.client.get(self.user_profile_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(UserProfile.objects.all().count(), 2)
        
    def test_staff_user_can_get_all_profiles(self):
        superuser = User.objects.create()
        superuser.is_superuser = True
        superuser.save()
        self.client.force_login(user=superuser)
        response = self.client.get(self.user_profile_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)
    
    def test_user_can_retrieve_their_profile_by_uuid(self):
        response = self.client.get(self.user_profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_retrieve_other_users_profile(self):
        self.client.force_login(user=self.seller)
        response = self.client.get(self.user_profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_their_profile(self):
        update_data = {
            'user': {'first_name': 'new_name'},
            'address': {}}
        self.client.put(self.user_profile_detail_url, data=update_data)
        response = self.client.get(self.user_profile_list_url)
        result = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['results'][0]['first_name'], update_data['user']['first_name'])
    
    def test_user_cannot_update_not_their_profile(self):
        self.client.force_login(user=self.seller)
        update_data = {
            'user': {'first_name': 'new_name'},
            'address': {}}
        response = self.client.put(self.user_profile_detail_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)