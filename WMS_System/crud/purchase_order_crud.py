from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import purchase_orders
from schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from database import database
from sqlalchemy import desc

async def generate_next_po_number():
    query = (
        select(purchase_orders.c.po_number)
        .order_by(desc(purchase_orders.c.id))
        .limit(1)
    )
    last_po = await database.fetch_one(query)

    if last_po and last_po["po_number"].startswith("PO-"):
        try:
            last_number = int(last_po["po_number"].split("-")[-1])
        except ValueError:
            last_number = 0
        new_number = last_number + 1
    else:
        new_number = 1

    return f"PO-{str(new_number).zfill(5)}"

# CREATE
async def create_purchase_order(po: PurchaseOrderCreate, current_user):
    values = po.dict()

    # Generate PO number if not provided
    if not values.get("po_number"):
        values["po_number"] = await generate_next_po_number()

    values["created_by"] = current_user

    query = insert(purchase_orders).values(**values)
    inserted_id = await database.execute(query)

    return {
        "id": inserted_id,
        "po_number": values["po_number"],
        "message": "Purchase Order created successfully.",
        "created by": current_user
    }


# GET ALL
async def get_all_purchase_orders():
    query = select(purchase_orders)
    return await database.fetch_all(query)


# GET BY ID
async def get_purchase_order_by_id(po_id: int):
    query = select(purchase_orders).where(purchase_orders.c.id == po_id)
    po = await database.fetch_one(query)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found.")
    return po


# UPDATE
async def update_purchase_order(po_id: int, updated_data: PurchaseOrderUpdate, current_user):
    query = select(purchase_orders).where(purchase_orders.c.id == po_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Purchase Order not found.")

    update_values = updated_data.dict(exclude_unset=True)
    update_values["modified_by"] = current_user["id"]
    query = (
        update(purchase_orders)
        .where(purchase_orders.c.id == po_id)
        .values(**update_values)
    )
    await database.execute(query)
    return {"message": "Purchase Order updated successfully."}


# DELETE
async def delete_purchase_order(po_id: int):
    query = delete(purchase_orders).where(purchase_orders.c.id == po_id)
    await database.execute(query)
    return {"message": "Purchase Order deleted successfully."}
