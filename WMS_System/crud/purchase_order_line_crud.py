from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import purchase_order_lines
from database import database
from schemas.purchase_order_line import PurchaseOrderLineCreate, PurchaseOrderLineUpdate


async def create_po_line(line_data: PurchaseOrderLineCreate):
    line_dict = line_data.dict()
    # Auto-calculate line total if not passed
    if line_dict["line_total"] == 0 and line_dict["unit_price"]:
        line_dict["line_total"] = line_dict["quantity"] * line_dict["unit_price"]

    insert_query = insert(purchase_order_lines).values(**line_dict)
    await database.execute(insert_query)
    return {"message": "Purchase Order Line created successfully."}


async def get_po_lines():
    return await database.fetch_all(select(purchase_order_lines))


async def get_po_line_by_id(line_id: int):
    query = select(purchase_order_lines).where(purchase_order_lines.c.id == line_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Line not found.")
    return result


async def get_lines_by_po_id(po_id: int):
    query = select(purchase_order_lines).where(purchase_order_lines.c.purchase_order_id == po_id)
    return await database.fetch_all(query)


async def update_po_line(line_id: int, line_data: PurchaseOrderLineUpdate):
    update_query = (
        update(purchase_order_lines)
        .where(purchase_order_lines.c.id == line_id)
        .values(**line_data.dict(exclude_unset=True))
        .returning(purchase_order_lines)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Line not found.")
    return updated


async def delete_po_line(line_id: int):
    delete_query = (
        delete(purchase_order_lines)
        .where(purchase_order_lines.c.id == line_id)
        .returning(purchase_order_lines)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Line not found.")
    return deleted
