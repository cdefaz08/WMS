from fastapi import HTTPException
from sqlalchemy import insert , select , update , delete
from models import location_types
from database import database  # Asegúrate de tener tu objeto `database`

#create Location Type
async def create_location_type(location_data):
    existing_query = select(location_types).where(location_types.c.location_type == location_data.location_type)
    existing = await database.fetch_one(existing_query)
    
    if existing:
        raise HTTPException(status_code=400, detail="Location type already exists")
    
    query = insert(location_types).values(**location_data.dict())
    try:
        await database.execute(query)
        return {"message": "Location type created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Get all location types
async def get_all_location_types():
    query = select(location_types)
    return await database.fetch_all(query)


# Update a location type with existence check
async def update_location_type(location_type_id: str, update_data):
    # 1. Verificar si existe
    check_query = select(location_types).where(location_types.c.location_type == location_type_id)
    existing = await database.fetch_one(check_query)

    if not existing:
        raise HTTPException(status_code=404, detail="Location type not found")

    # 2. Preparar los campos a actualizar
    values = {key: value for key, value in update_data.dict().items() if value is not None}
    if not values:
        raise HTTPException(status_code=400, detail="No fields to update")

    # 3. Ejecutar actualización
    query = (
        update(location_types)
        .where(location_types.c.location_type == location_type_id)
        .values(**values)
    )

    await database.execute(query)
    return {"message": "Location type updated successfully"}

async def get_location_type_by_id(location_type: str):
    query = location_types.select().where(location_types.c.location_type == location_type)
    result = await database.fetch_one(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Location type not found")

    # Convierte a dict y elimina las claves que no quieres retornar
    data = dict(result)
    data.pop("system_flag", None)
    data.pop("sto_pall_cart_flag", None)
    data.pop("mix_recdate_flag", None)

    return data

# Delete location type
async def delete_location_type(location_type_id: str):
    # 1. Verificar si existe
    check_query = select(location_types).where(location_types.c.location_type == location_type_id)
    existing = await database.fetch_one(check_query)

    if not existing:
        raise HTTPException(status_code=404, detail="Location type not found")

    # 2. Ejecutar eliminación
    query = delete(location_types).where(location_types.c.location_type == location_type_id)
    await database.execute(query)

    return {"message": "Location type deleted successfully"}
