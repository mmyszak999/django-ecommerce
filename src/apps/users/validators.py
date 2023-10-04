from typing import Any

from django.db.models import Model

from src.core.exceptions import IncorrectPasswords, ValueNotUniqueException

def validate_passwords(password: str, password_repeat: str):
    if password != repeat_password:
        raise IncorrectPasswords("Passwords don't match! Please sure that both passwords are the same!")


def validate_uniqueness(model: Model, field, value: Any):
    if not model.objects.get(field=value):
        raise ValueNotUniqueException(
            f"This value of {model._meta.get_field(field)} for model {model.__name__} is not unique!"
            "Please change the value!")