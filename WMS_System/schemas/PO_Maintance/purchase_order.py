from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class PurchaseOrderBase(BaseModel):
    po_number: Optional[str] = None
    vendor_id: int
    order_date: date
    expected_date: Optional[date] = None
    ship_date: Optional[date] = None
    status: Optional[str] = "Open"
    created_by: Optional[str] = None
    modified_by: Optional[str] = None

    # Dirección de envío (Ship From)
    ship_company_name: Optional[str] = None
    ship_address: Optional[str] = None
    ship_city: Optional[str] = None
    ship_state: Optional[str] = None
    ship_zip_code: Optional[str] = None
    ship_country: Optional[str] = None
    ship_contact_name: Optional[str] = None
    ship_contact_phone: Optional[str] = None
    ship_tax_id: Optional[str] = None

    # Dirección de facturación (Bill To)
    bill_company_name: Optional[str] = None
    bill_address: Optional[str] = None
    bill_city: Optional[str] = None
    bill_state: Optional[str] = None
    bill_zip_code: Optional[str] = None
    bill_country: Optional[str] = None
    bill_contact_name: Optional[str] = None
    bill_contact_phone: Optional[str] = None
    bill_tax_id: Optional[str] = None

    # Campos personalizados
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None
    custom_4: Optional[str] = None
    custom_5: Optional[str] = None

    comments: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    vendor_id: Optional[int] = None
    order_date: Optional[date] = None
    expected_date: Optional[date] = None
    ship_date: Optional[date] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None

    # Dirección de envío (Ship From)
    ship_company_name: Optional[str] = None
    ship_address: Optional[str] = None
    ship_city: Optional[str] = None
    ship_state: Optional[str] = None
    ship_zip_code: Optional[str] = None
    ship_country: Optional[str] = None
    ship_contact_name: Optional[str] = None
    ship_contact_phone: Optional[str] = None
    ship_tax_id: Optional[str] = None

    # Dirección de facturación (Bill To)
    bill_company_name: Optional[str] = None
    bill_address: Optional[str] = None
    bill_city: Optional[str] = None
    bill_state: Optional[str] = None
    bill_zip_code: Optional[str] = None
    bill_country: Optional[str] = None
    bill_contact_name: Optional[str] = None
    bill_contact_phone: Optional[str] = None
    bill_tax_id: Optional[str] = None

    # Campos personalizados
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    custom_3: Optional[str] = None
    custom_4: Optional[str] = None
    custom_5: Optional[str] = None

    comments: Optional[str] = None


    # Puedes permitir actualizar algunos otros campos si quieres

    # Ejemplo (opcional):
    # custom_1: Optional[str] = None
    # modified_by: Optional[str] = None


class PurchaseOrder(PurchaseOrderBase):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


class PurchaseOrderInDB(PurchaseOrder):
    class Config:
        from_attributes = True
