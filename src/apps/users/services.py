from typing import Any, OrderedDict

from django.contrib.auth import get_user_model
from django.db import transaction

from src.apps.users.models import UserProfile, UserAddress
from src.apps.users.serializers import UserAddressInputSerializer, UserInputSerializer
from src.apps.users.validators import validate_passwords, validate_uniqueness
from src.entities.users_entities import UserAddressEntity, UserProfileEntity



User = get_user_model()

class UserProfileCreateService:
    def create_user(self, user_data: dict[str, Any]) -> User:
        password = user_data.pop("password")
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        
        return user
    
    def user_address_create(self, dto: UserAddressEntity) -> UserAddress:
        return UserAddress.objects.create(**dto)
    
    @classmethod
    def _build_user_address_dto_from_request_data(cls, request_data: OrderedDict) -> UserAddressEntity:
        serializer = UserAddressInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserAddressEntity(**request_data)
        
    def user_profile_create(self, dto: UserProfileEntity, user_address: UserAddress, user: User) -> UserProfile:
        user_profile = UserProfile.objects.create(user=user, **dto)
        user_profile.address.add(user_address)
        return user_profile

    @classmethod
    def _build_user_profile_dto_from_request_data(cls, request_data: OrderedDict) -> UserProfileEntity:
        serializer = UserInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserProfileEntity(**request_data)

    def register_user(request_data: OrderedDict) -> UserProfile:
        user_data = request_data.pop("user")
        address_data = request_data.pop("address")
        
        validate_passwords(user_data['password'], user_data['password_repeat'])
        user_data.pop("password_repeat")
        validate_uniqueness(UserProfile, UserProfile.email, user_data['email']) # check if email is unique
        validate_uniqueness(UserProfile, UserProfile.username, user_data['username']) # check if username is unique
        
        user_address_dto = self._build_user_address_dto_from_request_data(address_data)
        user_profile_dto = self._build_user_profile_dto_from_request_data(user_data)
        user = self.create_user(data=user_data)
        address = self.user_address_create(data=user_address_dto)
        return self.user_profile_create(user_profile_dto, address, user)
        