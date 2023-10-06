from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CartItemEntity:
    quantity: int


@dataclass(frozen=True)
class CartItemUpdateEntity:
    quantity: Optional[int]