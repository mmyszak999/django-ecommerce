from typing import Any, OrderedDict
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.db import transaction

from src.apps.users.models import UserProfile, UserAddress
from src.apps.users.serializers import UserAddressInputSerializer, UserProfileInputSerializer
from src.apps.users.validators import validate_passwords
from src.core.exceptions import ValueNotUniqueException
from src.entities.users_entities import UserAddressEntity, UserProfileEntity


User = get_user_model()

class UserProfileCreateService:
    def create_user(self, user_data: dict[str, Any], password: str) -> User:
        user_data.pop('role')
        user_data.pop('phone_number')
        user = User.objects.create(password=password, **user_data)
        user.set_password(password)
        user.save()
        
        return user
    
    def user_address_create(self, dto: UserAddressEntity) -> UserAddress:
        print(dto)
        return UserAddress.objects.create(
            primary_address=dto.primary_address,
            secondary_address=dto.secondary_address,
            country=dto.country,
            state=dto.state,
            city=dto.city,
            zip_code=dto.zip_code
        )
    
    @classmethod
    def _build_user_address_dto_from_request_data(cls, request_data: OrderedDict) -> UserAddressEntity:
        serializer = UserAddressInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserAddressEntity(*data.values())
        
    def user_profile_create(self, dto: UserProfileEntity, user_address: UserAddress, user: User) -> UserProfile:
        user_profile = UserProfile.objects.create(
            user=user,
            username=dto.username,
            role=dto.role,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name
            )
        
        user_profile.address.add(user_address)
        print(UserAddress.objects.all())
        return user_profile

    @classmethod
    def _build_user_profile_dto_from_request_data(cls, request_data: list) -> UserProfileEntity:
        print(request_data)
        serializer = UserProfileInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserProfileEntity(*data.values())
    
    @transaction.atomic
    def register_user(self, request_data: OrderedDict) -> UserProfile:
        user_profile_data = request_data.pop("user")
        address_data = request_data.pop("address")
        passwords = request_data.pop("passwords")
        
        validate_passwords(passwords['password'], passwords['password_repeat'])
        user_data = deepcopy(user_profile_data)
        user = self.create_user(user_data=user_data, password=passwords['password'])
        del passwords
        
        email_check = UserProfile.objects.filter(email=user_profile_data['email'])
        username_check = UserProfile.objects.filter(username=user_profile_data['username'])
        
        if email_check:
            raise ValueNotUniqueException(UserProfile, "email", user_profile_data['email'])

        if username_check:
            raise ValueNotUniqueException(UserProfile, "username", user_profile_data['username'])
        
        user_address_dto = self._build_user_address_dto_from_request_data(address_data)
        user_profile_dto = self._build_user_profile_dto_from_request_data(user_profile_data)
        address = self.user_address_create(dto=user_address_dto)
        
        return self.user_profile_create(user_profile_dto, address, user)
        