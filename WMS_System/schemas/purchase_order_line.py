from pydantic import BaseModel
from typing import Optional


class PurchaseOrderLineBase(BaseModel):
    purchase_order_id: int
    item_id: int
    quantity: int
    unit_price: Optional[float] = 0.0
    line_total: Optional[float] = 0.0
    comments: Optional[str] = None


class PurchaseOrderLineCreate(PurchaseOrderLineBase):
    pass


class PurchaseOrderLineUpdate(BaseModel):
    quantity: Optional[int]
    unit_price: Optional[float]
    line_total: Optional[float]
    comments: Optional[str]


class PurchaseOrderLine(PurchaseOrderLineBase):
    id: int

    class Config:
        from_attributes = True
