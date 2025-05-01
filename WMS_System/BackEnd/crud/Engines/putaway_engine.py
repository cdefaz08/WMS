# crud/putaway_engine.py

from fastapi import HTTPException
from sqlalchemy import select
from models import locations, putaway_rule_steps,putaway_group_classes
from schemas.Engines.putaway_engine import PalletInfo
from database import database
from typing import List

async def get_steps_by_rule(rule_id: int) -> List[dict]:
    query = select(putaway_rule_steps).where(putaway_rule_steps.c.rule_id == rule_id).order_by(putaway_rule_steps.c.seq)
    steps = await database.fetch_all(query)
    return steps

# Async - calculate putaway
async def calculate_putaway(entry: PalletInfo, rule_id: int):
    # 1. Get all steps ordered by seq
    steps = await get_steps_by_rule(rule_id)

    if not steps:
        raise HTTPException(status_code=404, detail="No putaway steps defined")

    # 2. Loop through steps
    for step in steps:
        # Qualification Checks
        if step["UOM"] and step["UOM"] != entry.item_uom:
            continue

        # Calculate fill % (basic version)
        fill_percent = 100.0
        if entry.total_cubic:
            fill_percent = (entry.total_quantity / entry.total_cubic) * 100

        if fill_percent < step["min_percent"] or fill_percent > step["max_percent"]:
            continue

        if step["location_type_from"] and entry.location_type_from:
            if step["location_type_from"] != entry.location_type_from:
                continue

        # 3. Find candidate locations
        filters = []
        # Add normal filters
        if "location_type_to" in step and step["location_type_to"] != "(Ignore)":
            filters.append(locations.c.location_type == step["location_type_to"])

        # Add Putaway Group filter
        if "putaway_group" in step and step["putaway_group"] != "(Ignore)":
            # Look up classes inside the group
            query_classes = select(putaway_group_classes.c.class_name).where(
                putaway_group_classes.c.group_name == step["putaway_group"]
            )
            classes = await database.fetch_all(query_classes)
            class_names = [c["class_name"] for c in classes]

            if class_names:
                filters.append(locations.c.putaway_class.in_(class_names))


        query_locs = select(locations).where(*filters)
        locs = await database.fetch_all(query_locs)

        if not locs:
            continue

        # 4. Sort locations
        locs = sorted(locs, key=lambda loc: loc["palle_cap"] or 0)

        best_loc = locs[0]

        return {
            "success": True,
            "location_id": best_loc["location_id"],
            "message": f"Assigned by step {step['seq']}"
        }

    return {
        "success": False,
        "location_id": None,
        "location_name": None,
        "message": "No suitable location found"
    }
