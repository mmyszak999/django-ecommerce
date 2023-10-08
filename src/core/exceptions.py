from typing import Any

from django.db.models import Model


class ServiceException(Exception):
    pass


class IncorrectPasswordsException(ServiceException):
    def __init__(self) -> None:
        super().__init__(
            "Passwords don't match! Please sure that both passwords are the same!"
        )


class ValueNotUniqueException(ServiceException):
    def __init__(self, model: Model, field: str, value: Any) -> None:
        super().__init__(
            f"Value {value} of {field} for model {model.__name__} is not unique! "
            "Please change the value!"
        )


class MaxQuantityExceededException(ServiceException):
    def __init__(self, inventory_quantity: int, typed_quantity: int) -> None:
        super().__init__(
            f"Typed product quantity - {typed_quantity}, "
            f"exceeds the biggest possible amount you can add to your cart - {inventory_quantity}! "
            "Please change the quantity value and check if the product is not out of stock!"
        )
