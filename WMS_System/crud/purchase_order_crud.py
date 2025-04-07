from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import purchase_orders
from database import database
from schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate


async def create_purchase_order(po_data: PurchaseOrderCreate):
    query = select(purchase_orders).where(purchase_orders.c.po_number == po_data.po_number)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="PO number already exists.")

    insert_query = insert(purchase_orders).values(**po_data.dict())
    await database.execute(insert_query)
    return {"message": "Purchase Order created successfully."}


async def get_purchase_orders():
    return await database.fetch_all(select(purchase_orders))


async def get_purchase_order_by_id(po_id: int):
    query = select(purchase_orders).where(purchase_orders.c.id == po_id)
    po = await database.fetch_one(query)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found.")
    return po


async def update_purchase_order(po_id: int, po_data: PurchaseOrderUpdate):
    update_query = (
        update(purchase_orders)
        .where(purchase_orders.c.id == po_id)
        .values(**po_data.dict(exclude_unset=True))
        .returning(purchase_orders)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Purchase Order not found.")
    return updated


async def delete_purchase_order(po_id: int):
    delete_query = (
        delete(purchase_orders)
        .where(purchase_orders.c.id == po_id)
        .returning(purchase_orders)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Purchase Order not found.")
    return deleted
