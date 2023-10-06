from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OrderItemEntity:
    quantity: int


@dataclass(frozen=True)
class OrderItemUpdateEntity:
    quantity: Optional[int]


@dataclass(frozen=True)
class OrderEntity:
    pass


@dataclass(frozen=True)
class OrderUpdateEntity:
    pass
