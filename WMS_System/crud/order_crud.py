from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import orders
from database import database
from schemas.order import OrderCreate, OrderUpdate
from typing import Optional
from datetime import date
from sqlalchemy.sql import and_


async def create_order(order_data: OrderCreate, created_by: str):
    query = select(orders).where(orders.c.order_number == order_data.order_number)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Order number already exists.")

    insert_query = (
        insert(orders)
        .values(**order_data.dict(exclude_none=True),created_by=created_by)
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



async def search_orders(
    order_number: Optional[str] = None,
    customer_name: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[str] = None,
    document_form: Optional[str] = None,
    label_form: Optional[str] = None,
    order_type: Optional[str] = None,
    order_date_from: Optional[date] = None,
    order_date_to: Optional[date] = None,
    ship_date_from: Optional[date] = None,
    ship_date_to: Optional[date] = None
):
    query = select(orders)
    filters = []

    if order_number:
        filters.append(orders.c.order_number.ilike(f"%{order_number}%"))
    if customer_name:
        filters.append(orders.c.customer_name.ilike(f"%{customer_name}%"))
    if status:
        filters.append(orders.c.status.ilike(f"%{status}%"))
    if created_by:
        filters.append(orders.c.created_by.ilike(f"%{created_by}%"))
    if document_form:
        filters.append(orders.c.document_form.ilike(f"%{document_form}%"))
    if label_form:
        filters.append(orders.c.label_form.ilike(f"%{label_form}%"))
    if order_type:
        filters.append(orders.c.order_type.ilike(f"%{order_type}%"))

    if order_date_from:
        filters.append(orders.c.order_date >= order_date_from)
    if order_date_to:
        filters.append(orders.c.order_date <= order_date_to)
    if ship_date_from:
        filters.append(orders.c.ship_date >= ship_date_from)
    if ship_date_to:
        filters.append(orders.c.ship_date <= ship_date_to)

    if filters:
        query = query.where(and_(*filters))

    return await database.fetch_all(query)
