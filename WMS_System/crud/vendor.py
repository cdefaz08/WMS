from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import vendors
from database import database
from schemas.vendor import VendorCreate, VendorUpdate
from typing import Optional
from sqlalchemy import select, and_
from models import vendors
from database import database


async def create_vendor(vendor: VendorCreate):
    query = select(vendors).where(vendors.c.vendor_code == vendor.vendor_code)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Vendor code already exists.")

    insert_query = insert(vendors).values(**vendor.dict()).returning(vendors)
    created = await database.fetch_one(insert_query)
    return created



async def get_vendors():
    return await database.fetch_all(select(vendors))

async def get_vendor_by_id(vendor_id: int):
    query = select(vendors).where(vendors.c.id == vendor_id)
    vendor = await database.fetch_one(query)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


async def update_vendor(vendor_id: int, vendor_data: VendorUpdate):
    update_values = vendor_data.dict(exclude_unset=True)

    if not update_values:
        raise HTTPException(status_code=400, detail="No data provided to update.")

    update_query = (
        update(vendors)
        .where(vendors.c.id == vendor_id)
        .values(**update_values)
        .returning(vendors)
    )

    updated = await database.fetch_one(update_query)

    if not updated:
        raise HTTPException(status_code=404, detail="Vendor not found.")

    return updated





async def delete_vendor(vendor_id: int):
    delete_query = (
        delete(vendors)
        .where(vendors.c.id == vendor_id)
        .returning(vendors)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return deleted



async def search_vendors(
    vendor_code: Optional[str] = None,
    vendor_name: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    tax_id: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    zip_code: Optional[str] = None
):
    query = select(vendors)
    filters = []

    if vendor_code:
        filters.append(vendors.c.vendor_code.ilike(f"%{vendor_code}%"))
    if vendor_name:
        filters.append(vendors.c.vendor_name.ilike(f"%{vendor_name}%"))
    if contact_name:
        filters.append(vendors.c.contact_name.ilike(f"%{contact_name}%"))
    if phone:
        filters.append(vendors.c.phone.ilike(f"%{phone}%"))
    if email:
        filters.append(vendors.c.email.ilike(f"%{email}%"))
    if tax_id:
        filters.append(vendors.c.tax_id.ilike(f"%{tax_id}%"))
    if city:
        filters.append(vendors.c.city.ilike(f"%{city}%"))
    if state:
        filters.append(vendors.c.state.ilike(f"%{state}%"))
    if country:
        filters.append(vendors.c.country.ilike(f"%{country}%"))
    if zip_code:
        filters.append(vendors.c.zip_code.ilike(f"%{zip_code}%"))

    if filters:
        query = query.where(and_(*filters))

    return await database.fetch_all(query)
