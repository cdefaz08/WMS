from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import vendors
from database import database
from schemas.vendor import VendorCreate, VendorUpdate


async def create_vendor(vendor: VendorCreate):
    query = select(vendors).where(vendors.c.vendor_code == vendor.vendor_code)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Vendor code already exists.")

    insert_query = insert(vendors).values(**vendor.dict())
    await database.execute(insert_query)
    return {"message": "Vendor created successfully."}


async def get_vendors():
    return await database.fetch_all(select(vendors))

async def get_vendor_by_id(vendor_id: int):
    query = select(vendors).where(vendors.c.id == vendor_id)
    vendor = await database.fetch_one(query)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


async def update_vendor(vendor_id: int, vendor_data: VendorUpdate):
    update_query = (
        update(vendors)
        .where(vendors.c.id == vendor_id)
        .values(**vendor_data.dict(exclude_unset=True))
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
