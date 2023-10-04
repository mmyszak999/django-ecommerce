from dataclasses import dataclass

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField



@dataclass(frozen=True)
class UserAddressEntity:
    primary_address: str
    country: CountryField
    city: str
    zip_code: str
    secondary_address: str = None
    state: str = None


@dataclass(frozen=True)
class UserProfileEntity:
    username: str
    first_name: str
    last_name: str
    email: str
    role: str
    phone_number: PhoneNumberField