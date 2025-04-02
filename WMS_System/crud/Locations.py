from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from models import locations
from database import database
from schemas.locations import LocationBase, LocationUpdate  # Asegúrate de importar correctamente


# Create with existence check
async def create_location(location: LocationBase):
    # Verificar si ya existe
    check_query = select(locations).where(locations.c.location_id == location.location_id)
    existing = await database.fetch_one(check_query)

    if existing:
        raise HTTPException(status_code=400, detail="Location with this ID already exists")

    # Si no existe, crearla
    query = insert(locations).values(**location.dict())
    await database.execute(query)
    return {**location.dict(), "location_id": location.location_id}

# Read All
async def get_all_locations():
    query = select(locations)
    return await database.fetch_all(query)


# Read by ID
async def get_location_by_id(location_id: str):
    query = select(locations).where(locations.c.location_id == location_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return result


# Update by ID
async def update_location(location_id: str, location_data: LocationUpdate):
    update_data = location_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    query = (
        update(locations)
        .where(locations.c.location_id == location_id)
        .values(**update_data)
    )
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    return {**update_data, "location_id": location_id}


# Delete by ID
async def delete_location(location_id: str):
    query = delete(locations).where(locations.c.location_id == location_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}
