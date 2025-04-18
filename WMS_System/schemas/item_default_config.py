from pydantic import BaseModel
from typing import Optional

class ItemDefaultConfigBase(BaseModel):
    item_code: str
    putaway_group: Optional[str] = None
    restock_class: Optional[str] = None
    pick_class: Optional[str] = None

class ItemDefaultConfigCreate(ItemDefaultConfigBase):
    pass

class ItemDefaultConfigUpdate(BaseModel):
    putaway_group: Optional[str] = None
    restock_class: Optional[str] = None
    pick_class: Optional[str] = None

class ItemDefaultConfigOut(ItemDefaultConfigBase):
    id: int

    class Config:
        from_attributes = True
