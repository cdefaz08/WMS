from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import receipts
from schemas.receipt_schema import ReceiptCreate
from database import database
from datetime import datetime


# Crear un nuevo recibo
async def create_receipt(new_receipt: ReceiptCreate, created_by: int):
    # Validar que no exista un recibo con el mismo número
    query = select(receipts).where(receipts.c.receipt_number == new_receipt.receipt_number)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Receipt number already exists.")

    insert_query = insert(receipts).values({
        **new_receipt.dict(),
        "created_by": created_by,
        "created_date": datetime.utcnow()  # ✅ Add created date here
    })
    inserted_id = await database.execute(insert_query)

    return {"id": inserted_id, "message": "Receipt created successfully."}


# ✅ Obtener todos los recibos
async def get_all_receipts():
    query = select(receipts)
    return await database.fetch_all(query)


# ✅ Obtener recibo por ID
async def get_receipt_by_id(receipt_id: int):
    query = select(receipts).where(receipts.c.id == receipt_id)
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=404, detail="Receipt not found.")
    return result


# ✅ Obtener recibo por receipt_number
async def get_receipt_by_number(receipt_number: str):
    query = select(receipts).where(receipts.c.receipt_number == receipt_number)
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=404, detail="Receipt not found.")
    return result


# ✅ Actualizar recibo
async def update_receipt(receipt_id: int, updated_data: dict):
    query = update(receipts).where(receipts.c.id == receipt_id).values(**updated_data)
    await database.execute(query)
    return {"message": "Receipt updated successfully."}


# ✅ Eliminar recibo
async def delete_receipt(receipt_id: int):
    query = delete(receipts).where(receipts.c.id == receipt_id)
    await database.execute(query)
    return {"message": "Receipt deleted successfully."}


from typing import Optional
from sqlalchemy import and_
from datetime import date

async def search_receipts(
    receipt_number: Optional[str] = None,
    release_num: Optional[str] = None,
    vendor_name: Optional[str] = None,
    invoice_num: Optional[str] = None,
    po_id: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[str] = None,
    expected_from: Optional[date] = None,
    expected_to: Optional[date] = None,
    received_from: Optional[date] = None,
    received_to: Optional[date] = None,
):
    query = select(receipts)
    filters = []

    if receipt_number:
        filters.append(receipts.c.receipt_number.ilike(f"%{receipt_number}%"))
    if release_num:
        filters.append(receipts.c.release_num.ilike(f"%{release_num}%"))
    if vendor_name:
        filters.append(receipts.c.vendor_name.ilike(f"%{vendor_name}%"))
    if invoice_num:
        filters.append(receipts.c.invoice_num.ilike(f"%{invoice_num}%"))
    if po_id:
        filters.append(receipts.c.po_id.ilike(f"%{po_id}%"))
    if status:
        filters.append(receipts.c.status.ilike(f"%{status}%"))
    if created_by:
        filters.append(receipts.c.created_by.ilike(f"%{created_by}%"))
    if expected_from:
        filters.append(receipts.c.date_expected >= expected_from)
    if expected_to:
        filters.append(receipts.c.date_expected <= expected_to)
    if received_from:
        filters.append(receipts.c.date_received >= received_from)
    if received_to:
        filters.append(receipts.c.date_received <= received_to)

    if filters:
        query = query.where(and_(*filters))

    return await database.fetch_all(query)
