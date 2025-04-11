from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReceiptLineBase(BaseModel):
    receipt_number: str
    line_number: Optional[int]
    item_code: str
    description: Optional[str]
    upc: Optional[str]
    quantity_ordered: int
    quantity_expected: int
    quantity_received: int
    uom: Optional[str]
    unit_price: Optional[float]
    total_price: Optional[float]
    lot_number: Optional[str]
    expiration_date: Optional[datetime]
    location_received: Optional[str]
    comments: Optional[str]
    custom_1: Optional[str]
    custom_2: Optional[str]
    custom_3: Optional[str]

class ReceiptLineCreate(ReceiptLineBase):
    pass

class ReceiptLineUpdate(ReceiptLineBase):
    pass

class ReceiptLine(ReceiptLineBase):
    id: int

    class Config:
        from_attributes = True
