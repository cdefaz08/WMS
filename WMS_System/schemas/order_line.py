from pydantic import BaseModel
from typing import Optional


class OrderLineBase(BaseModel):
    order_id: int
    item_id: int
    quantity: int
    unit_price: Optional[float] = 0.0
    line_total: Optional[float] = 0.0
    comments: Optional[str] = None


class OrderLineCreate(OrderLineBase):
    pass


class OrderLineUpdate(BaseModel):
    quantity: Optional[int]
    unit_price: Optional[float]
    line_total: Optional[float]
    comments: Optional[str]


class OrderLine(OrderLineBase):
    id: int

    class Config:
        orm_mode = True
