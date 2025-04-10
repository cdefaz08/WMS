from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    order_date: datetime
    ship_date: Optional[datetime] = None
    status: Optional[str] = "Pending"
    total_amount: Optional[float] = 0.0
    created_by: Optional[int] = None
    comments: Optional[str] = None
    # ✅ Nuevos campos
    label_form: Optional[str] = None
    document_form: Optional[str] = None
    order_type: Optional[str] = None

class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str]
    order_date: Optional[datetime]
    ship_date: Optional[datetime]
    status: Optional[str]
    total_amount: Optional[float]
    created_by: Optional[int]
    comments: Optional[str]


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True
