from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import putaway_rules, pick_rules, restock_rules
from schemas.rules_steps import (
    PutawayRuleCreate, PutawayRuleUpdate,
    PickRuleCreate, PickRuleUpdate,
    RestockRuleCreate, RestockRuleUpdate
)
from database import database

# -------------------
# PUTAWAY RULES
# -------------------
async def create_putaway_rule(entry: PutawayRuleCreate):
    exists = await database.fetch_one(select(putaway_rules).where(putaway_rules.c.rule_name == entry.rule_name))
    if exists:
        raise HTTPException(status_code=400, detail="Putaway rule already exists.")
    query = insert(putaway_rules).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Putaway rule created successfully."}

async def get_all_putaway_rules():
    return await database.fetch_all(select(putaway_rules))

async def get_putaway_rule_by_id(rule_id: int):
    result = await database.fetch_one(select(putaway_rules).where(putaway_rules.c.id == rule_id))
    if not result:
        raise HTTPException(status_code=404, detail="Putaway rule not found.")
    return result

async def update_putaway_rule(rule_id: int, data: PutawayRuleUpdate):
    await database.execute(
        update(putaway_rules)
        .where(putaway_rules.c.id == rule_id)
        .values(**data.dict(exclude_unset=True))
    )

async def delete_putaway_rule(rule_id: int):
    await database.execute(delete(putaway_rules).where(putaway_rules.c.id == rule_id))


# -------------------
# PICK RULES
# -------------------
async def create_pick_rule(entry: PickRuleCreate):
    exists = await database.fetch_one(select(pick_rules).where(pick_rules.c.rule_name == entry.rule_name))
    if exists:
        raise HTTPException(status_code=400, detail="Pick rule already exists.")
    query = insert(pick_rules).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Pick rule created successfully."}

async def get_all_pick_rules():
    return await database.fetch_all(select(pick_rules))

async def get_pick_rule_by_id(rule_id: int):
    result = await database.fetch_one(select(pick_rules).where(pick_rules.c.id == rule_id))
    if not result:
        raise HTTPException(status_code=404, detail="Pick rule not found.")
    return result

async def update_pick_rule(rule_id: int, data: PickRuleUpdate):
    await database.execute(
        update(pick_rules)
        .where(pick_rules.c.id == rule_id)
        .values(**data.dict(exclude_unset=True))
    )

async def delete_pick_rule(rule_id: int):
    await database.execute(delete(pick_rules).where(pick_rules.c.id == rule_id))


# -------------------
# RESTOCK RULES
# -------------------
async def create_restock_rule(entry: RestockRuleCreate):
    exists = await database.fetch_one(select(restock_rules).where(restock_rules.c.rule_name == entry.rule_name))
    if exists:
        raise HTTPException(status_code=400, detail="Restock rule already exists.")
    query = insert(restock_rules).values(**entry.dict())
    inserted_id = await database.execute(query)
    return {"id": inserted_id, "message": "Restock rule created successfully."}

async def get_all_restock_rules():
    return await database.fetch_all(select(restock_rules))

async def get_restock_rule_by_id(rule_id: int):
    result = await database.fetch_one(select(restock_rules).where(restock_rules.c.id == rule_id))
    if not result:
        raise HTTPException(status_code=404, detail="Restock rule not found.")
    return result

async def update_restock_rule(rule_id: int, data: RestockRuleUpdate):
    await database.execute(
        update(restock_rules)
        .where(restock_rules.c.id == rule_id)
        .values(**data.dict(exclude_unset=True))
    )

async def delete_restock_rule(rule_id: int):
    await database.execute(delete(restock_rules).where(restock_rules.c.id == rule_id))
