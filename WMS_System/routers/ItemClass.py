
from fastapi import APIRouter
from schemas.ItemClass import ItemClassCreate
from crud import ItemClass as crud_item_class

router = APIRouter()

@router.post("/", response_model=dict)
async def create_item_class(new_class: ItemClassCreate):
    return await crud_item_class.create_item_class(new_class)

@router.get("/")
async def get_item_classes():
    return await crud_item_class.get_all_item_classes()
