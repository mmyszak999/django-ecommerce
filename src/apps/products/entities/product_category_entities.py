from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProductCategoryEntity:
    name: str


@dataclass(frozen=True)
class ProductCategoryUpdateEntity:
    name: Optional[str]
