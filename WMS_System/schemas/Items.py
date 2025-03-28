from pydantic import BaseModel
from typing import Optional

# 1. Base común (opcional pero recomendado)
class ItemBase(BaseModel):
    item_id: str
    description: str
    price: float
    upc: int
    color: Optional[str] = None
    size: Optional[str] = None
    item_class: Optional[str] = None
    alt_item_id1: Optional[int] = None
    alt_item_id2: Optional[int] = None
    description2: Optional[str] = None
    brand: Optional[str] = None
    style: Optional[str] = None
    is_offer: Optional[bool] = None
    default_cfg: Optional[str] = None
    custum1: Optional[str] = None
    custum2: Optional[str] = None
    custum3: Optional[str] = None
    custum4: Optional[str] = None
    custum5: Optional[str] = None
    custum6: Optional[str] = None

# 2. Para crear ítems (POST)
class ItemCreate(ItemBase):
    pass

# 3. Para leer ítems (GET, con ID)
class ItemRead(ItemBase):
    id: int

# 4. Para actualizar ítems (PUT/PATCH) — todos opcionales
class ItemUpdate(BaseModel):
    item_id: Optional[str]
    description: Optional[str]
    price: Optional[float]
    upc: Optional[int]
    color: Optional[str]
    size: Optional[str]
    item_class: Optional[str]
    alt_item_id1: Optional[int]
    alt_item_id2: Optional[int]
    description2: Optional[str]
    brand: Optional[str]
    style: Optional[str]
    is_offer: Optional[str]
    default_cfg: Optional[str]
    custum1: Optional[str]
    custum2: Optional[str]
    custum3: Optional[str]
    custum4: Optional[str]
    custum5: Optional[str]
    custum6: Optional[str]
