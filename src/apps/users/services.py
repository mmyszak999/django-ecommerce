from typing import Any, OrderedDict
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.db import transaction

from src.apps.users.models import UserProfile, UserAddress
from src.apps.users.serializers import (
    UserAddressInputSerializer,
    UserProfileInputSerializer,
    UpdateUserProfileInputSerializer,
    UpdateUserAddressInputSerializer,
    UpdateUserSerializer,
)

from src.apps.users.validators import validate_passwords
from src.core.exceptions import ValueNotUniqueException
from src.apps.users.entities.users_entities import (
    UserAddressEntity,
    UserProfileEntity,
    UserAddressUpdateEntity,
    UserProfileUpdateEntity,
)


User = get_user_model()


class UserProfileCreateService:
    def create_user(self, user_data: dict[str, Any], password: str) -> User:
        user_data.pop("role")
        user_data.pop("phone_number")
        user = User.objects.create(password=password, **user_data)
        user.set_password(password)
        user.save()

        return user

    def user_address_create(self, dto: UserAddressEntity) -> UserAddress:
        return UserAddress.objects.create(
            primary_address=dto.primary_address,
            secondary_address=dto.secondary_address,
            country=dto.country,
            state=dto.state,
            city=dto.city,
            zip_code=dto.zip_code,
        )

    @classmethod
    def _build_user_address_dto_from_request_data(
        cls, request_data: OrderedDict
    ) -> UserAddressEntity:
        serializer = UserAddressInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserAddressEntity(*data.values())

    def user_profile_create(
        self, dto: UserProfileEntity, user_address: UserAddress, user: User
    ) -> UserProfile:
        user_profile = UserProfile.objects.create(
            user=user,
            username=dto.username,
            role=dto.role,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone_number=dto.phone_number,
        )

        user_profile.address.add(user_address)
        return user_profile

    @classmethod
    def _build_user_profile_dto_from_request_data(
        cls, request_data: OrderedDict
    ) -> UserProfileEntity:
        serializer = UserProfileInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return UserProfileEntity(*data.values())

    @transaction.atomic
    def register_user(self, request_data: OrderedDict) -> UserProfile:
        user_profile_data = request_data.pop("user")
        address_data = request_data.pop("address")
        passwords = request_data.pop("passwords")

        validate_passwords(passwords["password"], passwords["password_repeat"])
        user_data = deepcopy(user_profile_data)
        user = self.create_user(user_data=user_data, password=passwords["password"])
        del passwords

        email_check = UserProfile.objects.filter(email=user_profile_data["email"])
        username_check = UserProfile.objects.filter(
            username=user_profile_data["username"]
        )

        if email_check:
            raise ValueNotUniqueException(
                UserProfile, "email", user_profile_data["email"]
            )

        if username_check:
            raise ValueNotUniqueException(
                UserProfile, "username", user_profile_data["username"]
            )

        user_address_dto = self._build_user_address_dto_from_request_data(address_data)
        user_profile_dto = self._build_user_profile_dto_from_request_data(
            user_profile_data
        )
        address = self.user_address_create(dto=user_address_dto)

        return self.user_profile_create(user_profile_dto, address, user)


class UserUpdateService:
    def user_address_update(
        self, instance: UserAddress, dto: UserAddressUpdateEntity
    ) -> UserAddress:
        instance.primary_address = dto.primary_address
        instance.secondary_address = dto.secondary_address
        instance.country = dto.country
        instance.state = dto.state
        instance.city = dto.city
        instance.zip_code = dto.zip_code
        instance.save()
        return instance

    @classmethod
    def _build_user_address_dto_from_request_data(
        cls, instance: UserAddress, request_data: OrderedDict
    ) -> UserAddressUpdateEntity:
        serializer = UpdateUserAddressInputSerializer(
            instance, data=request_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        return UserAddressUpdateEntity(
            primary_address=data.get("primary_address", instance.primary_address),
            secondary_address=data.get("secondary_address", instance.secondary_address),
            country=data.get("country", instance.country),
            state=data.get("state", instance.state),
            city=data.get("city", instance.city),
            zip_code=data.get("zip_code", instance.zip_code),
        )

    def user_profile_update(
        self, dto: UserProfileUpdateEntity, instance: UserProfile
    ) -> UserProfile:
        instance.username = dto.username
        instance.first_name = dto.first_name
        instance.last_name = dto.last_name
        instance.phone_number = dto.phone_number
        instance.save()

        return instance

    @classmethod
    def _build_user_profile_dto_from_request_data(
        cls, instance: UserProfile, request_data: OrderedDict
    ) -> UserProfileUpdateEntity:
        serializer = UpdateUserProfileInputSerializer(
            instance, data=request_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        return UserProfileUpdateEntity(
            username=data.get("username", instance.username),
            first_name=data.get("first_name", instance.first_name),
            last_name=data.get("last_name", instance.last_name),
            phone_number=data.get("phone_number", instance.phone_number),
        )

    @transaction.atomic
    def update_user(
        self, request_data: OrderedDict, instance: UserProfile
    ) -> UserProfile:
        user_profile_data = request_data.pop("user")
        address_data = request_data.pop("address")
        address_instance = instance.address.all()[0]

        username_check = UserProfile.objects.filter(
            username=user_profile_data.get("username")
        )

        if username_check:
            raise ValueNotUniqueException(
                UserProfile, "username", user_profile_data["username"]
            )

        user_address_dto = self._build_user_address_dto_from_request_data(
            address_instance, address_data
        )
        user_profile_dto = self._build_user_profile_dto_from_request_data(
            instance, user_profile_data
        )
        address = self.user_address_update(address_instance, dto=user_address_dto)
        return self.user_profile_update(user_profile_dto, instance)
