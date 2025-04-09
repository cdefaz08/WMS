from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import Order_type
from schemas.order_type import OrderTypeCreate, OrderTypeUpdate
from database import database

# CREATE
async def create_order_type(new_type: OrderTypeCreate):
    query = select(Order_type).where(Order_type.c.order_type == new_type.order_type)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Order type already exists.")
    
    insert_query = insert(Order_type).values(**new_type.dict())
    inserted_id = await database.execute(insert_query)
    return { "id": inserted_id, "message": "Order type created successfully." }

# GET ALL
async def get_all_order_types():
    query = select(Order_type)
    return await database.fetch_all(query)

# GET BY ID
async def get_order_type_by_id(type_id: int):
    query = select(Order_type).where(Order_type.c.id == type_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order type not found.")
    return result

# UPDATE
async def update_order_type(type_id: int, updated_data: OrderTypeUpdate):
    query = select(Order_type).where(Order_type.c.id == type_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Order type not found.")

    update_query = update(Order_type).where(Order_type.c.id == type_id).values(**updated_data.dict(exclude_unset=True))
    await database.execute(update_query)
    return { "message": "Order type updated successfully." }

# DELETE
async def delete_order_type(type_id: int):
    query = select(Order_type).where(Order_type.c.id == type_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Order type not found.")

    delete_query = delete(Order_type).where(Order_type.c.id == type_id)
    await database.execute(delete_query)
    return { "message": "Order type deleted successfully." }
