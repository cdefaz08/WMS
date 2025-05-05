from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import pallets
from schemas.ItemMaintace.Pallets import PalletCreate, PalletRead
from datetime import datetime
from database import database

# CREATE
async def create_pallet(data: dict):
    # Convert created_date if it's a string
    if isinstance(data.get("created_date"), str):
        data["created_date"] = datetime.fromisoformat(data["created_date"])

    query = insert(pallets).values(**data)
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Pallet created successfully."}

# GET ALL
async def get_all_pallets():
    query = select(pallets)
    return await database.fetch_all(query)

# GET BY ID
async def get_pallet_by_id(pallet_id: str):
    query = select(pallets).where(pallets.c.pallet_id == pallet_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Pallet not found.")
    return result

# UPDATE
async def update_pallet(pallet_id: str, updated_data: PalletCreate):
    query = select(pallets).where(pallets.c.pallet_id == pallet_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Pallet not found.")

    update_query = (
        update(pallets)
        .where(pallets.c.pallet_id == pallet_id)
        .values(**updated_data.dict())
    )
    await database.execute(update_query)
    return {"message": "Pallet updated successfully."}

# DELETE
async def delete_pallet(pallet_id: str):
    query = select(pallets).where(pallets.c.pallet_id == pallet_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Pallet not found.")

    delete_query = delete(pallets).where(pallets.c.pallet_id == pallet_id)
    await database.execute(delete_query)
    return {"message": "Pallet deleted successfully."}
