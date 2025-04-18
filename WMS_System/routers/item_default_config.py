from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Security.dependencies import get_current_user

from schemas.item_default_config import (
    ItemDefaultConfigCreate,
    ItemDefaultConfigUpdate,
    ItemDefaultConfigOut,
)
from crud import item_default_config as crud

router = APIRouter(
    prefix="/item-default-config",
    tags=["Item Default Config"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=dict)
async def create_config(entry: ItemDefaultConfigCreate):
    return await crud.create_item_default_config(entry)

@router.get("/", response_model=List[dict])
async def get_all_configs():
    return await crud.get_all_item_default_configs()

@router.get("/{item_code}", response_model=dict)
async def get_config_by_item_code(item_code: str):
    return await crud.get_item_default_config_by_item_code(item_code)

@router.put("/{item_code}", response_model=dict)
async def update_config(item_code: str, data: ItemDefaultConfigUpdate):
    await crud.update_item_default_config(item_code, data)
    return {"message": "Item default config updated successfully."}

@router.delete("/{item_code}", response_model=dict)
async def delete_config(item_code: str):
    await crud.delete_item_default_config(item_code)
    return {"message": "Item default config deleted successfully."}
