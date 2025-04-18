
from fastapi import APIRouter
from schemas.ItemMaintace.ItemClass import ItemClassCreate
from crud.ItemMaintance import ItemClass as crud_item_class

router = APIRouter()

@router.post("/", response_model=dict)
async def create_item_class(new_class: ItemClassCreate):
    return await crud_item_class.create_item_class(new_class)

@router.get("/")
async def get_item_classes():
    return await crud_item_class.get_all_item_classes()

@router.put("/{item_class_id}", response_model=dict)
async def update_item_class(item_class_id: int, new_data: ItemClassCreate):
    return await crud_item_class.update_item_class(item_class_id, new_data)

@router.delete("/{item_class_id}", response_model=dict)
async def delete_item_class(item_class_id: int):
    return await crud_item_class.delete_item_class(item_class_id)