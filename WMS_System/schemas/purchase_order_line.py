from pydantic import BaseModel
from typing import Optional


class PurchaseOrderLineBase(BaseModel):
    purchase_order_id: int
    item_id: int
    qty_ordered: int
    qty_received: int
    unit_price: Optional[float] = None
    line_total: Optional[float] = None
    comments: Optional[str] = None


class PurchaseOrderLineCreate(PurchaseOrderLineBase):
    pass


class PurchaseOrderLineUpdate(BaseModel):
    qty_received: Optional[int] = None
    unit_price: Optional[float] = None
    comments: Optional[str] = None


class PurchaseOrderLineInDB(PurchaseOrderLineBase):
    id: int

    class Config:
        from_attributes = True
