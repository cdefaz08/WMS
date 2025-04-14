from pydantic import BaseModel
from typing import Optional
from datetime import datetime , date


class PurchaseOrderBase(BaseModel):
    po_number: Optional[str] = None
    vendor_id: int
    order_date: date                         # <- CAMBIO
    expected_date: Optional[date] = None     # <- CAMBIO
    ship_date: Optional[date] = None         # <- CAMBIO
    status: Optional[str] = "Open"
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    comments: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrderUpdate(BaseModel):
    expected_date: Optional[date] = None
    ship_date: Optional[date] = None
    status: Optional[str] = None
    comments: Optional[str] = None

class PurchaseOrder(PurchaseOrderBase):
    id: int
    created_by: Optional[str]
    created_date: Optional[datetime]         # <- Esto sí puede quedarse en datetime
    modified_by: Optional[str]
    modified_date: Optional[datetime]


class PurchaseOrderInDB(PurchaseOrderBase):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    class Config:
        from_attributes = True
