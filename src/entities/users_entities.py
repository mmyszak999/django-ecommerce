from dataclasses import dataclass

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField



@dataclass(frozen=True)
class UserAddressEntity:
    primary_address: str
    secondary_address: str
    country: CountryField
    state: str
    city: str
    zip_code: str


@dataclass(frozen=True)
class UserProfileEntity:
    username: str
    role: str
    email: str
    first_name: str
    last_name: str
    phone_number = PhoneNumberField