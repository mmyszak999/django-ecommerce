from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from src.apps.users.models import UserAddress, UserProfile


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )
        read_only_fields = fields


class UserAddressOutputSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = (
            "id",
            "primary_address",
            "secondary_address",
            "country",
            "state",
            "city",
            "postalcode",
        )
        read_only_fields = fields


class RegistrationOutputSerializer(serializers.ModelSerializer):

    user = UserOutputSerializer(many=False, read_only=True)
    address = UserAddressOutputSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "phone_number",
            "address",
        )
        read_only_fields = fields


class UserAddressInputSerializer(serializers.Serializer):
    address_1 = serializers.CharField()
    address_2 = serializers.CharField(required=False)
    country = CountryField()
    state = serializers.CharField(required=False)
    city = serializers.CharField()
    postalcode = serializers.CharField()


class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )


class RegistrationInputSerializer(serializers.Serializer):
    user = UserInputSerializer(required=True)
    phone_number = serializers.CharField()
    address = UserAddressInputSerializer()
