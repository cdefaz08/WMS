from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import restock_classes, putaway_classes, pick_classes
from schemas.LocationMaintance.locationClases import (
    RestockClassCreate, RestockClassUpdate,
    PutawayClassCreate, PutawayClassUpdate,
    PickClassCreate, PickClassUpdate
)
from database import database

# ========== RESTOCK ==========
async def create_restock_class(new_class: RestockClassCreate):
    query = select(restock_classes).where(restock_classes.c.class_name == new_class.class_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Restock class already exists.")

    insert_query = insert(restock_classes).values(**new_class.dict())
    await database.execute(insert_query)
    return {"message": "Restock class created successfully."}


async def get_restock_classes():
    query = select(restock_classes)
    return await database.fetch_all(query)


async def update_restock_class(class_id: int, class_data: RestockClassUpdate):
    update_query = (
        update(restock_classes)
        .where(restock_classes.c.id == class_id)
        .values(**class_data.dict(exclude_unset=True))
        .returning(restock_classes)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Restock class not found.")
    return updated


async def delete_restock_class(class_id: int):
    delete_query = (
        delete(restock_classes)
        .where(restock_classes.c.id == class_id)
        .returning(restock_classes)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restock class not found.")
    return deleted


# ========== PUTAWAY ==========
async def create_putaway_class(new_class: PutawayClassCreate):
    query = select(putaway_classes).where(putaway_classes.c.class_name == new_class.class_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Putaway class already exists.")

    insert_query = insert(putaway_classes).values(**new_class.dict())
    await database.execute(insert_query)
    return {"message": "Putaway class created successfully."}


async def get_putaway_classes():
    query = select(putaway_classes)
    return await database.fetch_all(query)


async def update_putaway_class(class_id: int, class_data: PutawayClassUpdate):
    update_query = (
        update(putaway_classes)
        .where(putaway_classes.c.id == class_id)
        .values(**class_data.dict(exclude_unset=True))
        .returning(putaway_classes)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Putaway class not found.")
    return updated


async def delete_putaway_class(class_id: int):
    delete_query = (
        delete(putaway_classes)
        .where(putaway_classes.c.id == class_id)
        .returning(putaway_classes)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Putaway class not found.")
    return deleted


# ========== PICK ==========
async def create_pick_class(new_class: PickClassCreate):
    query = select(pick_classes).where(pick_classes.c.class_name == new_class.class_name)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Pick class already exists.")

    insert_query = insert(pick_classes).values(**new_class.dict())
    await database.execute(insert_query)
    return {"message": "Pick class created successfully."}


async def get_pick_classes():
    query = select(pick_classes)
    return await database.fetch_all(query)


async def update_pick_class(class_id: int, class_data: PickClassUpdate):
    update_query = (
        update(pick_classes)
        .where(pick_classes.c.id == class_id)
        .values(**class_data.dict(exclude_unset=True))
        .returning(pick_classes)
    )
    updated = await database.fetch_one(update_query)
    if not updated:
        raise HTTPException(status_code=404, detail="Pick class not found.")
    return updated


async def delete_pick_class(class_id: int):
    delete_query = (
        delete(pick_classes)
        .where(pick_classes.c.id == class_id)
        .returning(pick_classes)
    )
    deleted = await database.fetch_one(delete_query)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pick class not found.")
    return deleted
