from pydantic import BaseModel
from typing import Optional


class SaleLineBase(BaseModel):
    item_id: int
    item_code: Optional[str]
    description: Optional[str]
    quantity: float
    unit_price: float
    discount: float = 0.0
    line_total: float


class SaleLineCreate(SaleLineBase):
    pass


class SaleLine(SaleLineBase):
    id: int
    sale_id: int

    class Config:
        from_attributes = True
