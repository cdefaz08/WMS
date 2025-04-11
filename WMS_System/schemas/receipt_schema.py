from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReceiptBase(BaseModel):
    receipt_number: str
    po_id: Optional[int]= None
    vendor_id: Optional[int]= None
    received_by: Optional[str] = None
    receipt_date: datetime= None
    total_received_items: Optional[int]= None
    comments: Optional[str]= None

    vendor_name: Optional[str]= None
    release_num: Optional[str]= None
    invoice_num: Optional[str]= None
    status: Optional[str]= None
    date_shipped: Optional[datetime]= None
    date_expected: Optional[datetime]= None
    date_received: Optional[datetime]= None
    label_form: Optional[str]= None
    document_form: Optional[str]= None
    close_receipt: Optional[bool] = False
    carrier: Optional[str]= None
    seal_num: Optional[str]= None
    created_by: Optional[str]= None
    created_date: Optional[datetime]= None

    ship_from_company: Optional[str]= None
    ship_from_address: Optional[str]= None
    ship_from_address2: Optional[str]= None
    ship_from_city: Optional[str]= None
    ship_from_state: Optional[str]= None
    ship_from_zip: Optional[str]= None
    ship_from_country: Optional[str]= None
    ship_from_contact_name: Optional[str]= None
    ship_from_contact_phone: Optional[str]= None
    ship_from_tax_id: Optional[str]= None

    bill_to_company: Optional[str]= None
    bill_to_address: Optional[str]= None
    bill_to_address2: Optional[str]= None
    bill_to_city: Optional[str]= None
    bill_to_state: Optional[str]= None
    bill_to_zip: Optional[str]= None
    bill_to_country: Optional[str]= None
    bill_to_contact_name: Optional[str]= None
    bill_to_contact_phone: Optional[str]= None
    bill_to_tax_id: Optional[str]= None

    custom_1: Optional[str]= None
    custom_2: Optional[str]= None
    custom_3: Optional[str]= None
    custom_4: Optional[str]= None
    custom_5: Optional[str]= None
    custom_6: Optional[str]= None
    custom_7: Optional[str]= None
    custom_8: Optional[str]= None
    custom_9: Optional[str]= None
    custom_10: Optional[str]= None

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    id: int

    class Config:
        orm_mode = True
