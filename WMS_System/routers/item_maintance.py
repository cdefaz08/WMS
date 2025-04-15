# routes/item_maintance.py

from fastapi import APIRouter, HTTPException, Depends
from Security.dependencies import get_current_user
from schemas.ItemMaintance import ItemMaintanceCreate, ItemMaintanceUpdate, ItemMaintance,ItemConfigUOM
import crud.ItemMaintance as item_maintance_crud


router = APIRouter(prefix="/item-config", tags=["Item Configuration"],
    dependencies=[Depends(get_current_user)])


# ✅ Crear configuración
@router.post("/", response_model=dict)
async def create_item_configuration_endpoint(config: ItemMaintanceCreate):
    return await item_maintance_crud.create_item_configuration(config)


# ✅ Obtener todas las configuraciones
@router.get("/", response_model=list)
async def get_all_item_configurations_endpoint():
    return await item_maintance_crud.get_all_item_configurations()

@router.get("/items/{item_id}/configurations", response_model=list[ItemMaintance])
async def get_configurations_by_item(item_id: int):
    results = await item_maintance_crud.get_configurations_by_item_id(item_id)
    if not results:
        raise HTTPException(status_code=404, detail="No configurations found for this item.")
    return results

# ✅ Obtener configuración por ID
@router.get("/{config_id}", response_model=dict)
async def get_item_configuration_by_id_endpoint(config_id: int):
    return await item_maintance_crud.get_item_configuration_by_id(config_id)


# ✅ Actualizar configuración
@router.put("/{config_id}", response_model=dict)
async def update_item_configuration_endpoint(config_id: int, update_data: ItemMaintanceUpdate):
    return await item_maintance_crud.update_item_configuration(config_id, update_data)


# ✅ Eliminar configuración
@router.delete("/{config_id}", response_model=dict)
async def delete_item_configuration_endpoint(config_id: int):
    return await item_maintance_crud.delete_item_configuration(config_id)

@router.get("/item-maintance/default/{item_id}", response_model=ItemConfigUOM)
async def read_default_item_config(item_id: str):
    config = await item_maintance_crud.get_default_item_config_by_item_id(item_id)
    if not config:
        raise HTTPException(status_code=404, detail="Default item configuration not found.")
    return config
