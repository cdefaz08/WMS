from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import (
    putaway_group_classes, 
    pick_group_classes, 
    restock_group_classes
)
from schemas.RuleMaintance.group_classes import (
    PutawayGroupClassCreate, PutawayGroupClassUpdate,
    PickGroupClassCreate, PickGroupClassUpdate,
    RestockGroupClassCreate, RestockGroupClassUpdate
)
from database import database

# ----------------------------
# PUTAWAY GROUP CLASS METHODS
# ----------------------------
async def create_putaway_class(entry: PutawayGroupClassCreate):
    query = insert(putaway_group_classes).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Putaway group class created successfully."}

async def get_all_putaway_classes():
    query = select(putaway_group_classes)
    records = await database.fetch_all(query)
    return [dict(r) for r in records]

async def get_putaway_class_by_id(class_id: int):
    query = select(putaway_group_classes).where(putaway_group_classes.c.id == class_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Putaway group class not found.")
    return result

async def update_putaway_class(class_id: int, data: PutawayGroupClassUpdate):
    query = (
        update(putaway_group_classes)
        .where(putaway_group_classes.c.id == class_id)
        .values(**data.dict(exclude_unset=True))
    )
    await database.execute(query)

async def delete_putaway_class(class_id: int):
    query = delete(putaway_group_classes).where(putaway_group_classes.c.id == class_id)
    await database.execute(query)


# -----------------------
# PICK GROUP CLASS METHODS
# -----------------------
async def create_pick_class(entry: PickGroupClassCreate):
    query = insert(pick_group_classes).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Pick group class created successfully."}

async def get_all_pick_classes():
    query = select(pick_group_classes)
    records = await database.fetch_all(query)
    return [dict(r) for r in records]

async def get_pick_class_by_id(class_id: int):
    query = select(pick_group_classes).where(pick_group_classes.c.id == class_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Pick group class not found.")
    return result

async def update_pick_class(class_id: int, data: PickGroupClassUpdate):
    query = (
        update(pick_group_classes)
        .where(pick_group_classes.c.id == class_id)
        .values(**data.dict(exclude_unset=True))
    )
    await database.execute(query)

async def delete_pick_class(class_id: int):
    query = delete(pick_group_classes).where(pick_group_classes.c.id == class_id)
    await database.execute(query)


# --------------------------
# RESTOCK GROUP CLASS METHODS
# --------------------------
async def create_restock_class(entry: RestockGroupClassCreate):
    query = insert(restock_group_classes).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Restock group class created successfully."}

async def get_all_restock_classes():
    query = select(restock_group_classes)
    records = await database.fetch_all(query)
    return [dict(r) for r in records]

async def get_restock_class_by_id(class_id: int):
    query = select(restock_group_classes).where(restock_group_classes.c.id == class_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Restock group class not found.")
    return result

async def update_restock_class(class_id: int, data: RestockGroupClassUpdate):
    query = (
        update(restock_group_classes)
        .where(restock_group_classes.c.id == class_id)
        .values(**data.dict(exclude_unset=True))
    )
    await database.execute(query)

async def delete_restock_class(class_id: int):
    query = delete(restock_group_classes).where(restock_group_classes.c.id == class_id)
    await database.execute(query)
