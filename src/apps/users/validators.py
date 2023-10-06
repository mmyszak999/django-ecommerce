from typing import Any

from src.core.exceptions import IncorrectPasswordsException, ValueNotUniqueException

def validate_passwords(password: str, password_repeat: str):
    if password != password_repeat:
        raise IncorrectPasswordsException