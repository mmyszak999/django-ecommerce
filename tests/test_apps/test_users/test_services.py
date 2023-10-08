from django.contrib.auth import get_user_model
from django.test import TestCase

from src.apps.users.models import UserAddress, UserProfile
from src.apps.users.services import UserProfileCreateService, UserUpdateService

User = get_user_model()


class TestUserProfileCreateService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_service = UserProfileCreateService()
        cls.update_service = UserUpdateService()
        cls.user_profile_data = {
            "user": {
                "username": "test_user1",
                "email": "test_user1@mail.com",
                "first_name": "Name1",
                "last_name": "Name2",
                "role": "customer", 
                "phone_number": "+48123123123"
            },
            "passwords": {
                "password": "password123",
                "password_repeat": "password123",
            },
            "address": {
                "primary_address": "Kowalskiego 12",
                "country": "PL",
                "city": "Warsaw",
                "zip_code": "69-420"
            },
        }

        cls.update_user_profile_data = {
            "user": {
                "phone_number": "+48666777444",
            },
            "address": {

            },
        }
        
        cls.update_user_address_data = {
            "user": {
            },
            "address": {
                "country": "AZ",
                "city": "Kabul",
            },
        }

    def test_user_profile_create_service_correctly_creates_user(self):
        created_user = self.create_service.register_user(self.user_profile_data)

        self.assertEqual(UserProfile.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserAddress.objects.all().count(), 1)

        self.assertEqual(UserProfile.objects.get(id=created_user.id).id, created_user.id)

    def test_user_update_service_correctly_updates_user(self):
        user_profile = self.create_service.register_user(self.user_profile_data)
        user_profile = self.update_service.update_user(
            instance=user_profile, request_data=self.update_user_profile_data
        )

        self.assertEqual(UserProfile.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 1)

        self.assertEqual(UserProfile.objects.get(id=user_profile.id), user_profile)
        self.assertEqual(UserProfile.objects.get(id=user_profile.id).phone_number, user_profile.phone_number)

    def test_user_update_service_correctly_updates_user_address(self):
        user_profile = self.create_service.register_user(self.user_profile_data)
        user_profile = self.update_service.update_user(
            instance=user_profile, request_data=self.update_user_address_data
        )
        account_id = user_profile.id
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserAddress.objects.all().count(), 1)

        self.assertEqual(UserProfile.objects.get(id=account_id), user_profile)
        self.assertEqual(
            UserAddress.objects.first(), user_profile.address.first()
        )