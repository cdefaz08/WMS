from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import receipts
from schemas.receipt_schema import ReceiptCreate
from database import database


# ✅ Crear un nuevo recibo
async def create_receipt(new_receipt: ReceiptCreate):
    # Validar que no exista un recibo con el mismo número
    query = select(receipts).where(receipts.c.receipt_number == new_receipt.receipt_number)
    existing = await database.fetch_one(query)

    if existing:
        raise HTTPException(status_code=400, detail="Receipt number already exists.")

    insert_query = insert(receipts).values(**new_receipt.dict())
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
