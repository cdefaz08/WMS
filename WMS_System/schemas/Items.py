from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    item_id: str
    description: str
    color: Optional[str] = None
    size: Optional[str] = None
    price: float
    upc: int
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