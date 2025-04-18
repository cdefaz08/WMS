from fastapi import APIRouter, HTTPException,Depends
from Security.dependencies import get_current_user
from typing import List
from crud.RuleMaintance import rule_groups as crud_rules
from schemas.RuleMaintance.rules_groups import (
    PutawayGroupCreate, PutawayGroupUpdate,
    PickGroupCreate, PickGroupUpdate,
    RestockGroupCreate, RestockGroupUpdate
)

router = APIRouter(prefix="/rules", tags=["Rules"],
    dependencies=[Depends(get_current_user)])

# -----------------------
# PUTAWAY GROUPS ROUTES
# -----------------------

@router.post("/putaway-groups/", response_model=dict)
async def create_putaway_group(group: PutawayGroupCreate):
    return await crud_rules.create_putaway_group(group)

@router.get("/putaway-groups/", response_model=List[dict])
async def get_putaway_groups():
    return await crud_rules.get_putaway_groups()

@router.get("/putaway-groups/{group_id}", response_model=dict)
async def get_putaway_group_by_id(group_id: int):
    result = await crud_rules.get_putaway_group_by_id(group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Putaway group not found.")
    return result

@router.put("/putaway-groups/{group_id}", response_model=dict)
async def update_putaway_group(group_id: int, group: PutawayGroupUpdate):
    await crud_rules.update_putaway_group(group_id, group)
    return {"message": "Putaway group updated successfully."}

@router.delete("/putaway-groups/{group_id}", response_model=dict)
async def delete_putaway_group(group_id: int):
    await crud_rules.delete_putaway_group(group_id)
    return {"message": "Putaway group deleted successfully."}


# -----------------------
# PICK GROUPS ROUTES
# -----------------------

@router.post("/pick-groups/", response_model=dict)
async def create_pick_group(group: PickGroupCreate):
    return await crud_rules.create_pick_group(group)

@router.get("/pick-groups/", response_model=List[dict])
async def get_pick_groups():
    return await crud_rules.get_pick_groups()

@router.get("/pick-groups/{group_id}", response_model=dict)
async def get_pick_group_by_id(group_id: int):
    result = await crud_rules.get_pick_group_by_id(group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Pick group not found.")
    return result

@router.put("/pick-groups/{group_id}", response_model=dict)
async def update_pick_group(group_id: int, group: PickGroupUpdate):
    await crud_rules.update_pick_group(group_id, group)
    return {"message": "Pick group updated successfully."}

@router.delete("/pick-groups/{group_id}", response_model=dict)
async def delete_pick_group(group_id: int):
    await crud_rules.delete_pick_group(group_id)
    return {"message": "Pick group deleted successfully."}


# -----------------------
# RESTOCK GROUPS ROUTES
# -----------------------

@router.post("/restock-groups/", response_model=dict)
async def create_restock_group(group: RestockGroupCreate):
    return await crud_rules.create_restock_group(group)

@router.get("/restock-groups/", response_model=List[dict])
async def get_restock_groups():
    return await crud_rules.get_restock_groups()

@router.get("/restock-groups/{group_id}", response_model=dict)
async def get_restock_group_by_id(group_id: int):
    result = await crud_rules.get_restock_group_by_id(group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Restock group not found.")
    return result

@router.put("/restock-groups/{group_id}", response_model=dict)
async def update_restock_group(group_id: int, group: RestockGroupUpdate):
    await crud_rules.update_restock_group(group_id, group)
    return {"message": "Restock group updated successfully."}

@router.delete("/restock-groups/{group_id}", response_model=dict)
async def delete_restock_group(group_id: int):
    await crud_rules.delete_restock_group(group_id)
    return {"message": "Restock group deleted successfully."}
