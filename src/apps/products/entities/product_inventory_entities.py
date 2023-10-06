from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProductInventoryEntity:
    quantity: int


@dataclass(frozen=True)
class ProductInventoryUpdateEntity:
    quantity: Optional[int]
