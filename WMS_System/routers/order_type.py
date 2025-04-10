from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from schemas.order_type import OrderTypeCreate, OrderTypeUpdate
import crud.order_type as crud

router = APIRouter(prefix="/order_types", tags=["Order Types"],
    dependencies=[Depends(get_current_user)] )

@router.post("/")
async def create_order_type(new_type: OrderTypeCreate):
    return await crud.create_order_type(new_type)

@router.get("/")
async def get_all_order_types():
    return await crud.get_all_order_types()

@router.get("/{type_id}")
async def get_order_type_by_id(type_id: int):
    return await crud.get_order_type_by_id(type_id)

@router.put("/{type_id}")
async def update_order_type(type_id: int, updated: OrderTypeUpdate):
    return await crud.update_order_type(type_id, updated)

@router.delete("/{type_id}")
async def delete_order_type(type_id: int):
    return await crud.delete_order_type(type_id)
