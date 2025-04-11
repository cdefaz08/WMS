from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReceiptBase(BaseModel):
    receipt_number: str
    po_id: int
    vendor_id: int
    received_by: Optional[int]
    receipt_date: datetime
    total_received_items: Optional[int]
    comments: Optional[str]

    vendor_name: Optional[str]
    release_num: Optional[str]
    invoice_num: Optional[str]
    status: Optional[str]
    date_shipped: Optional[datetime]
    date_expected: Optional[datetime]
    date_received: Optional[datetime]
    label_form: Optional[str]
    document_form: Optional[str]
    close_receipt: Optional[bool] = False
    carrier: Optional[str]
    seal_num: Optional[str]
    created_by: Optional[int]
    created_date: Optional[datetime]

    ship_from_company: Optional[str]
    ship_from_address: Optional[str]
    ship_from_address2: Optional[str]
    ship_from_city: Optional[str]
    ship_from_state: Optional[str]
    ship_from_zip: Optional[str]
    ship_from_country: Optional[str]
    ship_from_contact_name: Optional[str]
    ship_from_contact_phone: Optional[str]
    ship_from_tax_id: Optional[str]

    bill_to_company: Optional[str]
    bill_to_address: Optional[str]
    bill_to_address2: Optional[str]
    bill_to_city: Optional[str]
    bill_to_state: Optional[str]
    bill_to_zip: Optional[str]
    bill_to_country: Optional[str]
    bill_to_contact_name: Optional[str]
    bill_to_contact_phone: Optional[str]
    bill_to_tax_id: Optional[str]

    custom_1: Optional[str]
    custom_2: Optional[str]
    custom_3: Optional[str]
    custom_4: Optional[str]
    custom_5: Optional[str]
    custom_6: Optional[str]
    custom_7: Optional[str]
    custom_8: Optional[str]
    custom_9: Optional[str]
    custom_10: Optional[str]

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    id: int

    class Config:
        orm_mode = True
