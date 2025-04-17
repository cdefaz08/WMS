from fastapi import APIRouter , Body, Query

from schemas.Items import ItemCreate, ItemUpdate,ItemOut
from crud import Items as crud_items
from typing import Optional


router = APIRouter()

#Create Item
@router.post("/", response_model=dict)
async def create_item(item: ItemCreate):
    return await crud_items.create_item(item)

#Read Selected Item

@router.get("/{item_id}")
async def get_item(item_id: int):
    return await crud_items.read_item(item_id)

@router.put("/{item_id}")
async def update_item(
    item_id: int,
    updated_data: ItemUpdate
):
    return await crud_items.update_item(item_id, updated_data.dict(exclude_unset=True))

#Delete item by item id
@router.delete("/{item_id}")
async def delete_item(item_id: int):
    return await crud_items.delete_item(item_id)

@router.get("/")
async def read_items(upc: int = Query(None)):
    if upc is not None:
        return await crud_items.get_item_by_upc(upc)
    return await crud_items.read_items()

@router.get("/upc/{upc}", response_model=ItemOut)
async def get_item_by_upc(upc: int):
    db_item = await crud_items.get_item_by_upc(upc)
    return ItemOut(**dict(db_item))  # <- esto es lo que faltaba


@router.get("/")
async def read_items(
    item_id: Optional[str] = Query(None),
    upc: Optional[str] = Query(None),
    alt_item_id1: Optional[str] = Query(None),
    alt_item_id2: Optional[str] = Query(None),
    item_class: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    brand: Optional[str] = Query(None)
):
    return await crud_items.search_items(
        item_id=item_id,
        upc=upc,
        alt_item_id1=alt_item_id1,
        alt_item_id2=alt_item_id2,
        item_class=item_class,
        color=color,
        size=size,
        brand=brand
    )
