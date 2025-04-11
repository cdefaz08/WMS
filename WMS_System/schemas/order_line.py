from pydantic import BaseModel
from typing import Optional

class OrderLineBase(BaseModel):
    order_number: str
    item_code: str
    upc: Optional[int]
    alt_item_id1: Optional[int] = None
    alt_item_id2: Optional[int]= None
    quantity: int
    unit_price: float
    line_total: float
    comments: Optional[str] = None

class OrderLineCreate(OrderLineBase):
    pass

class OrderLineUpdate(OrderLineBase):
    pass

class OrderLine(OrderLineBase):
    id: int

    class Config:
        from_attributes = True
