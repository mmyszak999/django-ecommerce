from dataclasses import dataclass
from decimal import Decimal
from io import BytesIO


@dataclass(frozen=True)
class ProductEntity:
    name: str
    price: Decimal
    description: str
    product_image: BytesIO


@dataclass(frozen=True)
class ProductUpdateEntity:
    name: Optional[str]
    price: Optional[Decimal]
    description: Optional[str]
    product_image: Optional[BytesIO]