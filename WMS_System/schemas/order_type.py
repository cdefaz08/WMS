from pydantic import BaseModel
from typing import Optional

class OrderTypeBase(BaseModel):
    order_type: str
    description: Optional[str] = None
    document_form: Optional[str] = None
    label_form : Optional[str] = None

class OrderTypeCreate(OrderTypeBase):
    pass

class OrderTypeUpdate(BaseModel):
    order_type: Optional[str] = None
    description: Optional[str] = None
    document_form: Optional[str] = None
    label_form : Optional[str] = None

class OrderType(OrderTypeBase):
    id: int

    class Config:
        from_attributes = True
