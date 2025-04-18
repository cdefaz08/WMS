from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import putaway_groups, pick_groups, restock_groups
from schemas.RuleMaintance.rules_groups import (
    PutawayGroupCreate, PutawayGroupUpdate,
    PickGroupCreate, PickGroupUpdate,
    RestockGroupCreate, RestockGroupUpdate
)
from database import database

# -----------------------
# PUTAWAY GROUPS
# -----------------------
async def create_putaway_group(new_group: PutawayGroupCreate):
    query = select(putaway_groups).where(putaway_groups.c.group_name == new_group.group_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Putaway group already exists.")

    insert_query = insert(putaway_groups).values(**new_group.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Putaway group created successfully."}


async def get_putaway_groups():
    query = select(putaway_groups)
    return await database.fetch_all(query)

async def get_putaway_group_by_id(group_id: int):
    query = select(putaway_groups).where(putaway_groups.c.id == group_id)
    return await database.fetch_one(query)

async def update_putaway_group(group_id: int, group: PutawayGroupUpdate):
    update_query = (
        update(putaway_groups)
        .where(putaway_groups.c.id == group_id)
        .values(**group.dict(exclude_unset=True))
    )
    await database.execute(update_query)

async def delete_putaway_group(group_id: int):
    delete_query = delete(putaway_groups).where(putaway_groups.c.id == group_id)
    await database.execute(delete_query)

# -----------------------
# PICK GROUPS
# -----------------------
async def create_pick_group(new_group: PickGroupCreate):
    query = select(pick_groups).where(pick_groups.c.group_name == new_group.group_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Pick group already exists.")

    insert_query = insert(pick_groups).values(**new_group.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Pick group created successfully."}


async def get_pick_groups():
    query = select(pick_groups)
    return await database.fetch_all(query)

async def get_pick_group_by_id(group_id: int):
    query = select(pick_groups).where(pick_groups.c.id == group_id)
    return await database.fetch_one(query)

async def update_pick_group(group_id: int, group: PickGroupUpdate):
    update_query = (
        update(pick_groups)
        .where(pick_groups.c.id == group_id)
        .values(**group.dict(exclude_unset=True))
    )
    await database.execute(update_query)

async def delete_pick_group(group_id: int):
    delete_query = delete(pick_groups).where(pick_groups.c.id == group_id)
    await database.execute(delete_query)

# -----------------------
# RESTOCK GROUPS
# -----------------------
async def create_restock_group(new_group: RestockGroupCreate):
    query = select(restock_groups).where(restock_groups.c.group_name == new_group.group_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Restock group already exists.")

    insert_query = insert(restock_groups).values(**new_group.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Restock group created successfully."}


async def get_restock_groups():
    query = select(restock_groups)
    return await database.fetch_all(query)

async def get_restock_group_by_id(group_id: int):
    query = select(restock_groups).where(restock_groups.c.id == group_id)
    return await database.fetch_one(query)

async def update_restock_group(group_id: int, group: RestockGroupUpdate):
    update_query = (
        update(restock_groups)
        .where(restock_groups.c.id == group_id)
        .values(**group.dict(exclude_unset=True))
    )
    await database.execute(update_query)

async def delete_restock_group(group_id: int):
    delete_query = delete(restock_groups).where(restock_groups.c.id == group_id)
    await database.execute(delete_query)
