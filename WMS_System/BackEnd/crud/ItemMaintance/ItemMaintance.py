# crud/item_maintance.py

from models import item_maintance
from database import database
from schemas.ItemMaintace.ItemMaintance import ItemMaintanceCreate, ItemMaintanceUpdate
from fastapi import HTTPException
from sqlalchemy import select


# ✅ Crear configuración
async def create_item_configuration(new_config: ItemMaintanceCreate):
    query = select(item_maintance).where(
        item_maintance.c.item_id == new_config.item_id,   # Cambiado a item_id
        item_maintance.c.is_default == True
    )

    # Validar que no haya más de un default por item_id
    if new_config.is_default:
        existing_default = await database.fetch_one(query)
        if existing_default:
            raise HTTPException(status_code=400, detail="Default configuration already exists for this item.")

    insert_query = item_maintance.insert().values(**new_config.dict())
    inserted_id = await database.execute(insert_query)
    return {"id": inserted_id, "message": "Item configuration created successfully."}


async def get_default_item_config_by_item_id(item_id: int):
    query = (
        select(
            item_maintance.c.item_id,
            item_maintance.c.boxes_per_pallet,
            item_maintance.c.pieces_per_case,
            item_maintance.c.configuration_name
        )
        .where(item_maintance.c.item_id == item_id)
        .where(item_maintance.c.is_default == True)
        .limit(1)
    )
    return await database.fetch_one(query)

# ✅ Obtener por ID
async def get_item_configuration_by_id(config_id: int):
    query = select(item_maintance).where(item_maintance.c.id == config_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item configuration not found.")
    return result

# ✅ Obtener todas las configuraciones de un ítem por item_id
async def get_configurations_by_item_id(item_id: int):
    query = select(item_maintance).where(item_maintance.c.item_id == item_id)
    results = await database.fetch_all(query)
    return results

# ✅ Obtener todas
async def get_all_item_configurations():
    query = select(item_maintance)
    return await database.fetch_all(query)


# ✅ Actualizar configuración
async def update_item_configuration(config_id: int, update_data: ItemMaintanceUpdate):
    query = item_maintance.update().where(item_maintance.c.id == config_id).values(**update_data.dict())
    result = await database.execute(query)
    return {"message": "Item configuration updated successfully."}


# ✅ Eliminar configuración
async def delete_item_configuration(config_id: int):
    query = item_maintance.delete().where(item_maintance.c.id == config_id)
    await database.execute(query)
    return {"message": "Item configuration deleted successfully."}
