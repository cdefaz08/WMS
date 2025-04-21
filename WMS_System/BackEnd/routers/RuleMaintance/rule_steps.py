from fastapi import APIRouter, Depends
from typing import List
from Security.dependencies import get_current_user
from schemas.RuleMaintance.rule_steps import (
    PutawayRuleStep, PutawayRuleStepCreate, PutawayRuleStepUpdate,
    PickRuleStep, PickRuleStepCreate, PickRuleStepUpdate,
    RestockRuleStep, RestockRuleStepCreate, RestockRuleStepUpdate
)
from crud.RuleMaintance import rule_steps as crud

router = APIRouter(
    prefix="/rules_steps",
    tags=["Rules Steps"],
    dependencies=[Depends(get_current_user)]
)

# ======== PUTAWAY ROUTES ========
@router.post("/putaway-rule-steps/", response_model=dict)
async def create_putaway_rule_step(entry: PutawayRuleStepCreate):
    return await crud.create_putaway_step(entry)

@router.get("/putaway-rule-steps/", response_model=List[PutawayRuleStep])
async def get_all_putaway_rule_steps():
    return await crud.get_all_putaway_steps()

@router.get("/putaway-rule-steps/{step_id}", response_model=PutawayRuleStep)
async def get_putaway_rule_step(step_id: int):
    return await crud.get_putaway_step_by_id(step_id)

@router.put("/putaway-rule-steps/{step_id}", response_model=dict)
async def update_putaway_rule_step(step_id: int, entry: PutawayRuleStepUpdate):
    return await crud.update_putaway_step(step_id, entry)

@router.delete("/putaway-rule-steps/{step_id}", response_model=dict)
async def delete_putaway_rule_step(step_id: int):
    return await crud.delete_putaway_step(step_id)


# ======== PICK ROUTES ========
@router.post("/pick-rule-steps/", response_model=dict)
async def create_pick_rule_step(entry: PickRuleStepCreate):
    return await crud.create_pick_step(entry)

@router.get("/pick-rule-steps/", response_model=List[PickRuleStep])
async def get_all_pick_rule_steps():
    return await crud.get_all_pick_steps()

@router.get("/pick-rule-steps/{step_id}", response_model=PickRuleStep)
async def get_pick_rule_step(step_id: int):
    return await crud.get_pick_step_by_id(step_id)

@router.put("/pick-rule-steps/{step_id}", response_model=dict)
async def update_pick_rule_step(step_id: int, entry: PickRuleStepUpdate):
    return await crud.update_pick_step(step_id, entry)

@router.delete("/pick-rule-steps/{step_id}", response_model=dict)
async def delete_pick_rule_step(step_id: int):
    return await crud.delete_pick_step(step_id)


# ======== RESTOCK ROUTES ========
@router.post("/restock-rule-steps/", response_model=dict)
async def create_restock_rule_step(entry: RestockRuleStepCreate):
    return await crud.create_restock_step(entry)

@router.get("/restock-rule-steps/", response_model=List[RestockRuleStep])
async def get_all_restock_rule_steps():
    return await crud.get_all_restock_steps()

@router.get("/restock-rule-steps/{step_id}", response_model=RestockRuleStep)
async def get_restock_rule_step(step_id: int):
    return await crud.get_restock_step_by_id(step_id)

@router.put("/restock-rule-steps/{step_id}", response_model=dict)
async def update_restock_rule_step(step_id: int, entry: RestockRuleStepUpdate):
    return await crud.update_restock_step(step_id, entry)

@router.delete("/restock-rule-steps/{step_id}", response_model=dict)
async def delete_restock_rule_step(step_id: int):
    return await crud.delete_restock_step(step_id)
