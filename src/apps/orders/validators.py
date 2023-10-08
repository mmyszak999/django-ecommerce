from src.core.exceptions import MaxQuantityExceededException


def validate_item_quantity(typed_quantity: int, max_quantity: int):
    if typed_quantity > max_quantity:
        raise MaxQuantityExceededException(max_quantity, typed_quantity)
