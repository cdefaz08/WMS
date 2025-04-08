from sqlalchemy import select, insert, update, delete
from models import proximities
from fastapi import HTTPException

# Create with existence check
async def create_proximity(database, proximity):
    check_query = select(proximities).where(proximities.c.proximity == proximity.proximity)
    existing = await database.fetch_one(check_query)

    if existing:
        raise HTTPException(status_code=400, detail="Proximity already exists")

    query = insert(proximities).values(**proximity.dict())
    await database.execute(query)
    return {**proximity.dict()}

# Read all
async def get_all_proximities(database):
    query = select(proximities)
    return await database.fetch_all(query)

# Update
async def update_proximity(database, proximity_id: int, proximity):
    check_query = select(proximities).where(proximities.c.id == proximity_id)
    existing = await database.fetch_one(check_query)

    if not existing:
        raise HTTPException(status_code=404, detail="Proximity not found")

    query = (
        update(proximities)
        .where(proximities.c.id == proximity_id)
        .values(**proximity.dict())
    )
    await database.execute(query)
    return {**proximity.dict(), "id": proximity_id}

# Delete
async def delete_proximity(database, proximity_id: int):
    query = delete(proximities).where(proximities.c.id == proximity_id)
    await database.execute(query)
    return {"message": "Proximity deleted"}

# Get by ID
async def get_proximity_by_id(database, proximity_id: int):
    query = select(proximities).where(proximities.c.id == proximity_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Proximity not found")
    return result

