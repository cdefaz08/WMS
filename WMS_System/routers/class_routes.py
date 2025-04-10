from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from crud import class_crud
from schemas.locationClases import (
    RestockClass, RestockClassCreate, RestockClassUpdate,
    PutawayClass, PutawayClassCreate, PutawayClassUpdate,
    PickClass, PickClassCreate, PickClassUpdate
)

router = APIRouter(prefix="/classes", tags=["Classes"],
    dependencies=[Depends(get_current_user)])


# ========== RESTOCK ==========
@router.post("/restock", response_model=RestockClass)
async def create_restock_class(class_data: RestockClassCreate):
    return await class_crud.create_restock_class(class_data)

@router.get("/restock", response_model=list[RestockClass])
async def read_restock_classes():
    return await class_crud.get_restock_classes()

@router.put("/restock/{class_id}", response_model=RestockClass)
async def update_restock_class(class_id: int, class_data: RestockClassUpdate):
    return await class_crud.update_restock_class(class_id, class_data)

@router.delete("/restock/{class_id}")
async def delete_restock_class(class_id: int):
    return await class_crud.delete_restock_class(class_id)


# ========== PUTAWAY ==========
@router.post("/putaway", response_model=PutawayClass)
async def create_putaway_class(class_data: PutawayClassCreate):
    return await class_crud.create_putaway_class(class_data)

@router.get("/putaway", response_model=list[PutawayClass])
async def read_putaway_classes():
    return await class_crud.get_putaway_classes()

@router.put("/putaway/{class_id}", response_model=PutawayClass)
async def update_putaway_class(class_id: int, class_data: PutawayClassUpdate):
    return await class_crud.update_putaway_class(class_id, class_data)

@router.delete("/putaway/{class_id}")
async def delete_putaway_class(class_id: int):
    return await class_crud.delete_putaway_class(class_id)


# ========== PICK ==========
@router.post("/pick", response_model=PickClass)
async def create_pick_class(class_data: PickClassCreate):
    return await class_crud.create_pick_class(class_data)

@router.get("/pick", response_model=list[PickClass])
async def read_pick_classes():
    return await class_crud.get_pick_classes()

@router.put("/pick/{class_id}", response_model=PickClass)
async def update_pick_class(class_id: int, class_data: PickClassUpdate):
    return await class_crud.update_pick_class(class_id, class_data)

@router.delete("/pick/{class_id}")
async def delete_pick_class(class_id: int):
    return await class_crud.delete_pick_class(class_id)
