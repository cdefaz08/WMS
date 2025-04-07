from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import order_lines
from database import database
from schemas.order_line import OrderLineCreate, OrderLineUpdate


async def create_order_line(line_data: OrderLineCreate):
    data = line_data.dict()
    if data["line_total"] == 0 and data["unit_price"]:
        data["line_total"] = data["quantity"] * data["unit_price"]

    insert_query = insert(order_lines).values(**data)
    await database.execute(insert_query)
    return {"message": "Order line created successfully."}


async def get_order_lines():
    return await database.fetch_all(select(order_lines))


async def get_order_line_by_id(line_id: int):
    query = select(order_lines).where(order_lines.c.id == line_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order line not found.")
    return result


async def get_lines_by_order_id(order_id: int):
    query = select(order_lines).where(order_lines.c.order_id == order_id)
    return await database.fetch_all(query)


async def update_order_line(line_id: int, line_data: OrderLineUpdate):
    update_query = (
        update(order_lines)
        .where(order_lines.c.id == line_id)
        .values(**line_data.dict(exclude_unset=True))
        .returning(order_lines)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Order line not found.")
    return updated


async def delete_order_line(line_id: int):
    delete_query = (
        delete(order_lines)
        .where(order_lines.c.id == line_id)
        .returning(order_lines)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order line not found.")
    return deleted
