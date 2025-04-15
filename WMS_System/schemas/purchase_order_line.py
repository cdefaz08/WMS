from pydantic import BaseModel
from typing import Optional
from datetime import date


class PurchaseOrderLineBase(BaseModel):
    purchase_order_id: int
    line_number: Optional[int] = None
    upc: Optional[str] = None
    item_id: int
    item_code: str
    description: Optional[str] = None
    qty_ordered: int
    qty_expected: Optional[int] = None
    qty_received: int
    uom: Optional[str] = "Pieces"
    unit_price: Optional[float] = None
    line_total: Optional[float] = None
    total_pieces: float  # 👈 nuevo campo
    lot_number: Optional[str] = None
    expiration_date: Optional[date] = None
    location_received: Optional[str] = None
    comments: Optional[str] = None
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None



class PurchaseOrderLineCreate(PurchaseOrderLineBase):
    pass


class PurchaseOrderLineUpdate(BaseModel):
    qty_received: Optional[int] = None
    unit_price: Optional[float] = None
    line_total: Optional[float] = None
    total_pieces: Optional[float] = None  # 👈 aquí también
    comments: Optional[str] = None
    lot_number: Optional[str] = None
    expiration_date: Optional[date] = None
    location_received: Optional[str] = None
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None


class PurchaseOrderLineInDB(PurchaseOrderLineBase):
    id: int

    class Config:
        from_attributes = True
