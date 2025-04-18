from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Security.dependencies import get_current_user

from schemas.group_classes import (
    PutawayGroupClassCreate, PutawayGroupClassUpdate,
    PickGroupClassCreate, PickGroupClassUpdate,
    RestockGroupClassCreate, RestockGroupClassUpdate
)

from crud import group_classes as crud

router = APIRouter(
    prefix="/group-classes",
    tags=["Group Classes"],
    dependencies=[Depends(get_current_user)]
)

# -----------------------------
# PUTAWAY GROUP CLASSES ROUTES
# -----------------------------

@router.post("/putaway/", response_model=dict)
async def create_putaway_class(entry: PutawayGroupClassCreate):
    return await crud.create_putaway_class(entry)

@router.get("/putaway/", response_model=List[dict])
async def get_all_putaway_classes():
    return await crud.get_all_putaway_classes()

@router.get("/putaway/{class_id}", response_model=dict)
async def get_putaway_class_by_id(class_id: int):
    return await crud.get_putaway_class_by_id(class_id)

@router.put("/putaway/{class_id}", response_model=dict)
async def update_putaway_class(class_id: int, data: PutawayGroupClassUpdate):
    await crud.update_putaway_class(class_id, data)
    return {"message": "Putaway group class updated successfully."}

@router.delete("/putaway/{class_id}", response_model=dict)
async def delete_putaway_class(class_id: int):
    await crud.delete_putaway_class(class_id)
    return {"message": "Putaway group class deleted successfully."}


# --------------------------
# PICK GROUP CLASSES ROUTES
# --------------------------

@router.post("/pick/", response_model=dict)
async def create_pick_class(entry: PickGroupClassCreate):
    return await crud.create_pick_class(entry)

@router.get("/pick/", response_model=List[dict])
async def get_all_pick_classes():
    return await crud.get_all_pick_classes()

@router.get("/pick/{class_id}", response_model=dict)
async def get_pick_class_by_id(class_id: int):
    return await crud.get_pick_class_by_id(class_id)

@router.put("/pick/{class_id}", response_model=dict)
async def update_pick_class(class_id: int, data: PickGroupClassUpdate):
    await crud.update_pick_class(class_id, data)
    return {"message": "Pick group class updated successfully."}

@router.delete("/pick/{class_id}", response_model=dict)
async def delete_pick_class(class_id: int):
    await crud.delete_pick_class(class_id)
    return {"message": "Pick group class deleted successfully."}


# -----------------------------
# RESTOCK GROUP CLASSES ROUTES
# -----------------------------

@router.post("/restock/", response_model=dict)
async def create_restock_class(entry: RestockGroupClassCreate):
    return await crud.create_restock_class(entry)

@router.get("/restock/", response_model=List[dict])
async def get_all_restock_classes():
    return await crud.get_all_restock_classes()

@router.get("/restock/{class_id}", response_model=dict)
async def get_restock_class_by_id(class_id: int):
    return await crud.get_restock_class_by_id(class_id)

@router.put("/restock/{class_id}", response_model=dict)
async def update_restock_class(class_id: int, data: RestockGroupClassUpdate):
    await crud.update_restock_class(class_id, data)
    return {"message": "Restock group class updated successfully."}

@router.delete("/restock/{class_id}", response_model=dict)
async def delete_restock_class(class_id: int):
    await crud.delete_restock_class(class_id)
    return {"message": "Restock group class deleted successfully."}
