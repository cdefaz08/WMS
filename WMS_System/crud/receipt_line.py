from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import receipt_lines
from schemas.receipt_line_schema import ReceiptLineCreate
from database import database
from datetime import datetime


# 🔹 Crear una nueva línea de recibo
async def create_receipt_line(new_line: ReceiptLineCreate):
    insert_query = insert(receipt_lines).values(**new_line.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Receipt line created successfully."}


# 🔹 Obtener todas las líneas
async def get_all_receipt_lines():
    query = select(receipt_lines)
    return await database.fetch_all(query)


# 🔹 Obtener línea por ID
async def get_receipt_line_by_id(line_id: int):
    query = select(receipt_lines).where(receipt_lines.c.id == line_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Receipt line not found.")
    return result


# 🔹 Obtener líneas por número de recibo
async def get_receipt_lines_by_receipt_number(receipt_number: str):
    query = select(receipt_lines).where(receipt_lines.c.receipt_number == receipt_number)
    return await database.fetch_all(query)


def parse_datetime(val):
    if isinstance(val, datetime):
        return val
    try:
        return datetime.fromisoformat(val)
    except:
        return None

async def update_receipt_line(line_id: int, updated_data: dict):
    if "expiration_date" in updated_data:
        updated_data["expiration_date"] = parse_datetime(updated_data["expiration_date"])

    query = update(receipt_lines).where(receipt_lines.c.id == line_id).values(**updated_data)
    await database.execute(query)
    return {"message": "Receipt line updated successfully."}


# 🔹 Eliminar línea de recibo
async def delete_receipt_line(line_id: int):
    query = delete(receipt_lines).where(receipt_lines.c.id == line_id)
    await database.execute(query)
    return {"message": "Receipt line deleted successfully."}

async def delete_receipt_lines_by_number(receipt_number: str):
    query = delete(receipt_lines).where(receipt_lines.c.receipt_number == receipt_number)
    await database.execute(query)
    return {"message": f"All receipt lines for receipt_number {receipt_number} deleted."}