from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import a_contents
from schemas.a_contents import AContentsCreate, AContentsUpdate
from database import database

# CREATE
async def create_a_content(entry: AContentsCreate):
    query = insert(a_contents).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Inventory content created successfully."}

# GET ALL
async def get_all_a_contents():
    query = select(a_contents)
    return await database.fetch_all(query)

# GET BY ID
async def get_a_content_by_id(content_id: int):
    query = select(a_contents).where(a_contents.c.id == content_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Inventory content not found.")
    return result

# UPDATE
async def update_a_content(content_id: int, updated_data: AContentsUpdate):
    query = select(a_contents).where(a_contents.c.id == content_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Inventory content not found.")

    update_query = (
        update(a_contents)
        .where(a_contents.c.id == content_id)
        .values(**updated_data.dict(exclude_unset=True))
    )
    await database.execute(update_query)
    return {"id": content_id, "message": "Inventory content updated successfully."}

# DELETE
async def delete_a_content(content_id: int):
    query = select(a_contents).where(a_contents.c.id == content_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Inventory content not found.")

    delete_query = delete(a_contents).where(a_contents.c.id == content_id)
    await database.execute(delete_query)
    return {"id": content_id, "message": "Inventory content deleted successfully."}

from typing import Optional, List

async def get_filtered_a_contents(
    location_id: Optional[str] = None,
    pallet_id: Optional[str] = None,
    item_id: Optional[str] = None,
    receipt_info: Optional[str] = None,
    receipt_release_num: Optional[str] = None,
) -> List[dict]:
    query = select(a_contents)

    if location_id:
        query = query.where(a_contents.c.location_id == location_id)
    if pallet_id:
        query = query.where(a_contents.c.pallet_id == pallet_id)
    if item_id:
        query = query.where(a_contents.c.item_id.ilike(f"%{item_id}%"))
    if receipt_info:
        query = query.where(a_contents.c.receipt_info.ilike(f"%{receipt_info}%"))
    if receipt_release_num:
        query = query.where(a_contents.c.receipt_release_num.ilike(f"%{receipt_release_num}%"))

    return await database.fetch_all(query)

async def get_by_exact_location_id(location_id: str) -> List[dict]:
    query = select(a_contents).where(a_contents.c.location_id == location_id)
    results = await database.fetch_all(query)
    return [dict(row) for row in results]

