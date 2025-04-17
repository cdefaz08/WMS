from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import purchase_order_lines
from schemas.purchase_order_line import (
    PurchaseOrderLineCreate,
    PurchaseOrderLineUpdate
)
from database import database


# CREATE
async def create_purchase_order_line(line: PurchaseOrderLineCreate):
    values = line.dict()
    if values.get("qty_ordered") and values.get("unit_price"):
        values["line_total"] = values["qty_ordered"] * (values["unit_price"] or 0)
    query = insert(purchase_order_lines).values(**values)
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Purchase order line created successfully."}


# GET ALL
async def get_all_purchase_order_lines():
    query = select(purchase_order_lines)
    return await database.fetch_all(query)


# GET BY ID
async def get_purchase_order_line_by_id(line_id: int):
    query = select(purchase_order_lines).where(purchase_order_lines.c.id == line_id)
    line = await database.fetch_one(query)
    if not line:
        raise HTTPException(status_code=404, detail="Purchase order line not found.")
    return line


# GET BY PO ID
async def get_lines_by_po_id(po_id: int):
    query = select(purchase_order_lines).where(purchase_order_lines.c.purchase_order_id == po_id)
    return await database.fetch_all(query)


# UPDATE
async def update_purchase_order_line(line_id: int, updated_data: PurchaseOrderLineUpdate):
    # 1. Validar existencia de la línea
    query = select(purchase_order_lines).where(purchase_order_lines.c.id == line_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Purchase order line not found.")

    # 2. Filtrar solo campos enviados
    update_values = updated_data.dict(exclude_unset=True)

    if not update_values:
        return {"message": "No fields provided to update."}

    # 3. Calcular line_total si se envió qty o unit_price
    if "total_pieces" in update_values or "unit_price" in update_values:
        pieces = update_values.get("total_pieces", existing["total_pieces"])
        price = update_values.get("unit_price", existing["unit_price"] or 0.0)
        update_values["line_total"] = float(pieces) * float(price)

    # 4. Ejecutar el UPDATE dinámico
    query = (
        update(purchase_order_lines)
        .where(purchase_order_lines.c.id == line_id)
        .values(**update_values)
    )
    await database.execute(query)
    return {"message": "Purchase order line updated successfully."}


# DELETE
async def delete_purchase_order_line(line_id: int):
    query = delete(purchase_order_lines).where(purchase_order_lines.c.id == line_id)
    await database.execute(query)
    return {"message": "Purchase order line deleted successfully."}

async def delete_lines_by_po_id(po_id: int):
    query = delete(purchase_order_lines).where(purchase_order_lines.c.purchase_order_id == po_id)
    await database.execute(query)