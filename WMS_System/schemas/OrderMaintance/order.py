from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    order_date: Optional[datetime] = None
    ship_date: Optional[datetime] = None
    status: Optional[str] = "Pending"
    total_amount: Optional[float] = 0.0
    created_by: Optional[str] = None
    comments: Optional[str] = None

    label_form: Optional[str] = None
    document_form: Optional[str] = None
    order_type: Optional[str] = None
    carrier: Optional[str] = None
    ship_method: Optional[str] = None
    customer_PO: Optional[str] = None

    shp_to_Company: Optional[str] = None
    shp_to_Addres: Optional[str] = None
    shp_to_City: Optional[str] = None
    shp_to_State: Optional[str] = None
    shp_to_ZipCode: Optional[str] = None
    shp_to_Country: Optional[str] = None
    shp_to_ContactName: Optional[str] = None
    shp_to_ContactPhone: Optional[str] = None
    shp_to_TaxId: Optional[str] = None

    bill_to_Company: Optional[str] = None
    bill_to_Addres: Optional[str] = None
    bill_to_City: Optional[str] = None
    bill_to_State: Optional[str] = None
    bill_to_ZipCode: Optional[str] = None
    bill_to_Country: Optional[str] = None
    bill_to_ContactName: Optional[str] = None
    bill_to_ContactPhone: Optional[str] = None
    bill_to_TaxId: Optional[str] = None

    InvoiceNumber: Optional[str] = None
    Store: Optional[str] = None
    Vendor_num: Optional[str] = None

    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None
    custom_4: Optional[str] = None
    custom_5: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_name: Optional[str]= None
    order_date: Optional[datetime]= None
    ship_date: Optional[datetime]= None
    status: Optional[str]= None
    total_amount: Optional[float]= None
    created_by: Optional[str]= None
    comments: Optional[str]= None

    label_form: Optional[str] = None
    document_form: Optional[str] = None
    order_type: Optional[str] = None
    carrier: Optional[str] = None
    Ship_method: Optional[str] = None
    customer_PO: Optional[str] = None

    shp_to_Company: Optional[str] = None
    shp_to_Addres: Optional[str] = None
    shp_to_Addres2 : Optional[str] = None
    shp_to_City: Optional[str] = None
    shp_to_State: Optional[str] = None
    shp_to_ZipCode: Optional[str] = None
    shp_to_Country: Optional[str] = None
    shp_to_ContactName: Optional[str] = None
    shp_to_ContactPhone: Optional[str] = None
    shp_to_TaxId: Optional[str] = None

    bill_to_Company: Optional[str] = None
    bill_to_Addres: Optional[str] = None
    bill_to_Address2: Optional[str] = None
    bill_to_City: Optional[str] = None
    bill_to_State: Optional[str] = None
    bill_to_ZipCode: Optional[str] = None
    bill_to_Country: Optional[str] = None
    bill_to_ContactName: Optional[str] = None
    bill_to_ContactPhone: Optional[str] = None
    bill_to_TaxId: Optional[str] = None

    InvoiceNumber: Optional[str] = None
    Store: Optional[str] = None
    Vendor_num: Optional[str] = None

    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None
    custom_4: Optional[str] = None
    custom_5: Optional[str] = None

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True
