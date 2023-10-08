from django.db import models
from django.contrib.auth.models import User
import uuid

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from src.apps.users.enums import UserRole


class UserAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    primary_address = models.CharField(max_length=200, blank=True, null=True)
    secondary_address = models.CharField(max_length=200, blank=True, null=True)
    country = CountryField()
    state = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"Address: {self.primary_address}, {self.city}, {self.country}"


class UserProfile(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(unique=True)
    role = models.CharField(choices=UserRole.choices())
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField()
    address = models.ManyToManyField(UserAddress, related_name="userprofile")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
