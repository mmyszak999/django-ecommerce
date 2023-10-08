from dataclasses import dataclass
from typing import Optional

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


@dataclass(frozen=True)
class UserAddressEntity:
    primary_address: str
    country: CountryField
    city: str
    zip_code: str
    secondary_address: Optional[str] = None
    state: Optional[str] = None


@dataclass(frozen=True)
class UserAddressUpdateEntity:
    primary_address: Optional[str]
    country: Optional[CountryField]
    city: Optional[str]
    zip_code: Optional[str]
    secondary_address: Optional[str]
    state: Optional[str]


@dataclass(frozen=True)
class UserProfileEntity:
    username: str
    first_name: str
    last_name: str
    email: str
    role: str
    phone_number: PhoneNumberField


@dataclass(frozen=True)
class UserProfileUpdateEntity:
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[PhoneNumberField]
