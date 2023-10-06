from dataclasses import dataclass
from decimal import Optional


@dataclass(frozen=True)
class ProductCategoryEntity:
    name: str


@dataclass(frozen=True)
class ProductCategoryUpdateEntity:
    name: Optional[str]
