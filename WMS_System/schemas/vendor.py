from pydantic import BaseModel
from typing import Optional


class VendorBase(BaseModel):
    vendor_code: str
    vendor_name: str
    contact_name: Optional[str] = None
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    notes: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    vendor_name: Optional[str]
    contact_name: Optional[str]
    tax_id: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    notes: Optional[str]


class Vendor(VendorBase):
    id: int

    class Config:
        from_attributes = True
