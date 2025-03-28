from fastapi import APIRouter , Body
from schemas.Items import ItemCreate, ItemUpdate
from crud import Items as crud_items


router = APIRouter()
#Create Item
@router.post("/", response_model=dict)
async def create_item(item: ItemCreate):
    return await crud_items.create_item(item)

# Read all the items NO FILTER
@router.get("/")
async def read_items():
    return await crud_items.read_items()

#Read Selected Item

@router.get("/{item_id}")
async def get_item(item_id: int):
    return await crud_items.read_item(item_id)

@router.put("/{item_id}")
async def update_item(
    item_id: int,
    updated_data: ItemUpdate = Body(...)
):
    return await crud_items.update_item(item_id, updated_data.dict(exclude_unset=True))



#Delete item by item id
@router.delete("/{item_id}")
async def delete_item(item_id: int):
    return await crud_items.delete_item(item_id)