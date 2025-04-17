from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReceiptLineBase(BaseModel):
    receipt_number: str
    line_number: Optional[int]
    item_code: str
    item_id: int
    description: Optional[str]
    upc: Optional[str]
    quantity_ordered: float
    quantity_expected: float
    quantity_received: float
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
    item_code: Optional[str] 
    item_id: Optional[int]
    description: Optional[str]
    upc: Optional[str]
    quantity_ordered: Optional[float]
    quantity_expected: Optional[float]
    quantity_received: Optional[float]
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

class ReceiptLine(ReceiptLineBase):
    id: int

    class Config:
        from_attributes = True
