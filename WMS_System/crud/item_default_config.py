from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import item_default_config
from schemas.item_default_config import ItemDefaultConfigCreate, ItemDefaultConfigUpdate
from database import database


# CREATE
async def create_item_default_config(entry: ItemDefaultConfigCreate):
    # Check if already exists by item_code
    query = select(item_default_config).where(item_default_config.c.item_code == entry.item_code)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Item default config already exists.")

    insert_query = insert(item_default_config).values(**entry.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Item default config created successfully."}

# GET ALL
async def get_all_item_default_configs():
    query = select(item_default_config)
    return await database.fetch_all(query)

# GET BY ITEM CODE
async def get_item_default_config_by_item_code(item_code: str):
    query = select(item_default_config).where(item_default_config.c.item_code == item_code)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item config not found.")
    return result

# UPDATE
async def update_item_default_config(item_code: str, data: ItemDefaultConfigUpdate):
    query = (
        update(item_default_config)
        .where(item_default_config.c.item_code == item_code)
        .values(**data.dict(exclude_unset=True))
    )
    await database.execute(query)

# DELETE
async def delete_item_default_config(item_code: str):
    query = delete(item_default_config).where(item_default_config.c.item_code == item_code)
    await database.execute(query)
