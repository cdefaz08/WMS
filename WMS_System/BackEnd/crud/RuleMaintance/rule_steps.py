from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import putaway_rule_steps, pick_rule_steps, restock_rule_steps
from schemas.RuleMaintance.rule_steps import (
    PutawayRuleStepCreate, PutawayRuleStepUpdate,
    PickRuleStepCreate, PickRuleStepUpdate,
    RestockRuleStepCreate, RestockRuleStepUpdate
)
from database import database


# ========== PUTAWAY ==========
async def create_putaway_step(entry: PutawayRuleStepCreate):
    query = insert(putaway_rule_steps).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Putaway rule step created successfully."}


async def get_all_putaway_steps():
    query = select(putaway_rule_steps)
    return await database.fetch_all(query)


async def get_putaway_step_by_id(step_id: int):
    query = select(putaway_rule_steps).where(putaway_rule_steps.c.id == step_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Putaway rule step not found.")
    return result


async def update_putaway_step(step_id: int, updated_data: PutawayRuleStepUpdate):
    query = (
        update(putaway_rule_steps)
        .where(putaway_rule_steps.c.id == step_id)
        .values(**updated_data.dict(exclude_unset=True))
    )
    await database.execute(query)
    return {"message": "Putaway rule step updated successfully."}


async def delete_putaway_step(step_id: int):
    query = delete(putaway_rule_steps).where(putaway_rule_steps.c.id == step_id)
    await database.execute(query)
    return {"message": "Putaway rule step deleted successfully."}


# ========== PICK ==========
async def create_pick_step(entry: PickRuleStepCreate):
    query = insert(pick_rule_steps).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Pick rule step created successfully."}


async def get_all_pick_steps():
    query = select(pick_rule_steps)
    return await database.fetch_all(query)


async def get_pick_step_by_id(step_id: int):
    query = select(pick_rule_steps).where(pick_rule_steps.c.id == step_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Pick rule step not found.")
    return result


async def update_pick_step(step_id: int, updated_data: PickRuleStepUpdate):
    query = (
        update(pick_rule_steps)
        .where(pick_rule_steps.c.id == step_id)
        .values(**updated_data.dict(exclude_unset=True))
    )
    await database.execute(query)
    return {"message": "Pick rule step updated successfully."}


async def delete_pick_step(step_id: int):
    query = delete(pick_rule_steps).where(pick_rule_steps.c.id == step_id)
    await database.execute(query)
    return {"message": "Pick rule step deleted successfully."}


# ========== RESTOCK ==========
async def create_restock_step(entry: RestockRuleStepCreate):
    query = insert(restock_rule_steps).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Restock rule step created successfully."}


async def get_all_restock_steps():
    query = select(restock_rule_steps)
    return await database.fetch_all(query)


async def get_restock_step_by_id(step_id: int):
    query = select(restock_rule_steps).where(restock_rule_steps.c.id == step_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Restock rule step not found.")
    return result


async def update_restock_step(step_id: int, updated_data: RestockRuleStepUpdate):
    query = (
        update(restock_rule_steps)
        .where(restock_rule_steps.c.id == step_id)
        .values(**updated_data.dict(exclude_unset=True))
    )
    await database.execute(query)
    return {"message": "Restock rule step updated successfully."}


async def delete_restock_step(step_id: int):
    query = delete(restock_rule_steps).where(restock_rule_steps.c.id == step_id)
    await database.execute(query)
    return {"message": "Restock rule step deleted successfully."}
