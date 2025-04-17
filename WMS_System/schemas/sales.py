from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .sale_lines import SaleLineCreate, SaleLine


class SaleBase(BaseModel):
    customer_name: Optional[str]
    customer_contact: Optional[str]
    payment_method: str
    subtotal: float
    tax: float = 0.0
    discount_total: float = 0.0
    total: float
    amount_received: float
    change_due: float
    created_by: str


class SaleCreate(SaleBase):
    lines: List[SaleLineCreate]


class Sale(SaleBase):
    id: int
    sale_number: str
    created_date: datetime
    lines: List[SaleLine] = []

    class Config:
        from_attributes = True
