from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PurchaseOrderBase(BaseModel):
    po_number: str
    vendor_id: int
    order_date: datetime
    expected_date: Optional[datetime] = None
    status: Optional[str] = "Open"
    created_by: Optional[int] = None
    comments: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    vendor_id: Optional[int]
    order_date: Optional[datetime]
    expected_date: Optional[datetime]
    status: Optional[str]
    created_by: Optional[int]
    comments: Optional[str]


class PurchaseOrder(PurchaseOrderBase):
    id: int

    class Config:
        from_attributes = True
