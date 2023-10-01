from django.db import models
from django.contrib.auth.models import User
import uuid

from django_countries.fields import CountryField

from django_ecommerce.apps.users.enums import UserRole


class UserAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    primary_address = models.CharField(max_length=200, blank=True, null=True)
    secondary_address = models.CharField(max_length=200, blank=True, null=True)
    country = CountryField()
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=25)

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
    role = models.CharField(choices=UserRole.choices)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.ManyToManyField(UserAddress, related_name="userprofile")
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"