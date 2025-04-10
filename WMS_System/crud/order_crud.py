from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import orders
from database import database
from schemas.order import OrderCreate, OrderUpdate


async def create_order(order_data: OrderCreate):
    query = select(orders).where(orders.c.order_number == order_data.order_number)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Order number already exists.")

    insert_query = (
        insert(orders)
        .values(**order_data.dict())
        .returning(orders)  # <- Return full order row
    )
    new_order = await database.fetch_one(insert_query)
    return new_order


async def get_orders():
    return await database.fetch_all(select(orders))


async def get_order_by_id(order_id: int):
    query = select(orders).where(orders.c.id == order_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found.")
    return result


async def update_order(order_id: int, order_data: OrderUpdate):
    update_query = (
        update(orders)
        .where(orders.c.id == order_id)
        .values(**order_data.dict(exclude_unset=True))
        .returning(orders)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found.")
    return updated


async def delete_order(order_id: int):
    delete_query = (
        delete(orders)
        .where(orders.c.id == order_id)
        .returning(orders)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found.")
    return deleted
