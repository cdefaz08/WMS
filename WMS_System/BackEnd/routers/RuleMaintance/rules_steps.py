from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Security.dependencies import get_current_user
from schemas.RuleMaintance.rules_steps import *
from crud.RuleMaintance import rules_steps as crud

router = APIRouter(
    prefix="/rules_steps",
    tags=["Rules Steps"],
    dependencies=[Depends(get_current_user)]
)

# --- PUTAWAY ---
@router.post("/putaway/", response_model=dict)
async def create_putaway_rule(rule: PutawayRuleCreate):
    return await crud.create_putaway_rule(rule)

@router.get("/putaway/", response_model=List[dict])
async def get_all_putaway_rules():
    return await crud.get_all_putaway_rules()

@router.get("/putaway/{rule_id}", response_model=dict)
async def get_putaway_rule_by_id(rule_id: int):
    return await crud.get_putaway_rule_by_id(rule_id)

@router.put("/putaway/{rule_id}", response_model=dict)
async def update_putaway_rule(rule_id: int, rule: PutawayRuleUpdate):
    await crud.update_putaway_rule(rule_id, rule)
    return {"message": "Putaway rule updated successfully."}

@router.delete("/putaway/{rule_id}", response_model=dict)
async def delete_putaway_rule(rule_id: int):
    await crud.delete_putaway_rule(rule_id)
    return {"message": "Putaway rule deleted successfully."}


# --- PICK ---
@router.post("/pick/", response_model=dict)
async def create_pick_rule(rule: PickRuleCreate):
    return await crud.create_pick_rule(rule)

@router.get("/pick/", response_model=List[dict])
async def get_all_pick_rules():
    return await crud.get_all_pick_rules()

@router.get("/pick/{rule_id}", response_model=dict)
async def get_pick_rule_by_id(rule_id: int):
    return await crud.get_pick_rule_by_id(rule_id)

@router.put("/pick/{rule_id}", response_model=dict)
async def update_pick_rule(rule_id: int, rule: PickRuleUpdate):
    await crud.update_pick_rule(rule_id, rule)
    return {"message": "Pick rule updated successfully."}

@router.delete("/pick/{rule_id}", response_model=dict)
async def delete_pick_rule(rule_id: int):
    await crud.delete_pick_rule(rule_id)
    return {"message": "Pick rule deleted successfully."}


# --- RESTOCK ---
@router.post("/restock/", response_model=dict)
async def create_restock_rule(rule: RestockRuleCreate):
    return await crud.create_restock_rule(rule)

@router.get("/restock/", response_model=List[dict])
async def get_all_restock_rules():
    return await crud.get_all_restock_rules()

@router.get("/restock/{rule_id}", response_model=dict)
async def get_restock_rule_by_id(rule_id: int):
    return await crud.get_restock_rule_by_id(rule_id)

@router.put("/restock/{rule_id}", response_model=dict)
async def update_restock_rule(rule_id: int, rule: RestockRuleUpdate):
    await crud.update_restock_rule(rule_id, rule)
    return {"message": "Restock rule updated successfully."}

@router.delete("/restock/{rule_id}", response_model=dict)
async def delete_restock_rule(rule_id: int):
    await crud.delete_restock_rule(rule_id)
    return {"message": "Restock rule deleted successfully."}
