from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class ProductCategoryEntity:
    name: str


@dataclass(frozen=True)
class ProductInventoryEntity:
    quantity: int
    sold: int
    
    
@dataclass(frozen=True)
class ProductEntity:
    name: str
    price: Decimal
    description: str