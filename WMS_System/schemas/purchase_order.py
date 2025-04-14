from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PurchaseOrderBase(BaseModel):
    po_number: Optional[str] = None
    vendor_id: int
    order_date: datetime
    expected_date: Optional[datetime] = None
    ship_date: Optional[datetime] = None
    status: Optional[str] = "Open"
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    comments: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    expected_date: Optional[datetime] = None
    ship_date: Optional[datetime] = None
    status: Optional[str] = None
    modified_by: Optional[str] = None
    comments: Optional[str] = None


class PurchaseOrderInDB(PurchaseOrderBase):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    class Config:
        from_attributes = True
