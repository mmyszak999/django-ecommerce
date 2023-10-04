from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from src.apps.users.models import UserAddress, UserProfile
from src.apps.users.enums import UserRole


class UserAddressInputSerializer(serializers.Serializer):
    primary_address = serializers.CharField()
    secondary_address = serializers.CharField(required=False)
    country = CountryField()
    state = serializers.CharField(required=False)
    city = serializers.CharField()
    zip_code = serializers.CharField()


class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    

class UserPasswordsSerializer(serializers.Serializer):
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


class UserProfileInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=UserRole.choices())
    phone_number = serializers.CharField()
    
    
class RegistrationInputSerializer(serializers.Serializer):
    user = UserProfileInputSerializer()
    passwords = UserPasswordsSerializer()
    address = UserAddressInputSerializer()
    

class UpdateUserProfileInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    address = UserAddressInputSerializer(required=False)
    
    
class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
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
            "zip_code",
        )
        read_only_fields = fields


class RegistrationOutputSerializer(serializers.ModelSerializer):

    user = UserOutputSerializer(many=False, read_only=True)
    address = UserAddressOutputSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "address",
            "phone_number",
            "role"
        )
        read_only_fields = fields


class UserProfileListOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(many=False, read_only=True)
    address = UserAddressOutputSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "phone_number",
            "address",
            'role',
        )
        read_only_fields = fields

class UserOrderOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "phone_number")
        read_only_fields = fields
