from fastapi import APIRouter, HTTPException
from typing import List

from schemas.LocationMaintance.locations import LocationBase, LocationUpdate

from crud.LocationMaintance.Locations import (
    create_location,
    get_all_locations,
    get_location_by_id,
    update_location,
    delete_location,search_locations
)

router = APIRouter()

# Create
@router.post("", response_model=LocationBase)
async def create_new_location(location: LocationBase):
    return await create_location(location)

# Read All
from typing import Optional

@router.get("", response_model=List[LocationBase])
async def read_all_locations(
    location_id: Optional[str] = None,
    aisle: Optional[str] = None,
    bay: Optional[str] = None,
    loc_level: Optional[str] = None,
    slot: Optional[str] = None,
    putaway_class: Optional[str] = None,
    rstk_class: Optional[str] = None,
    pick_class: Optional[str] = None,
    blocked_code: Optional[str] = None,
    location_type: Optional[str] = None,
    proximiti_in: Optional[str] = None,
    proximiti_out: Optional[str] = None
):
    return await search_locations(
        location_id=location_id,
        aisle=aisle,
        bay=bay,
        loc_level=loc_level,
        slot=slot,
        putaway_class=putaway_class,
        rstk_class=rstk_class,
        pick_class=pick_class,
        blocked_code=blocked_code,
        location_type=location_type,
        proximiti_in=proximiti_in,
        proximiti_out=proximiti_out
    )


# Read by ID
@router.get("/{location_id}", response_model=LocationBase)
async def read_location_by_id(location_id: str):
    return await get_location_by_id(location_id)

# Update by ID
@router.put("/{location_id}", response_model=LocationUpdate)
async def update_location_by_id(location_id: str, location: LocationUpdate):
    return await update_location(location_id, location)

# Delete by ID
@router.delete("/{location_id}")
async def delete_location_by_id(location_id: str):
    return await delete_location(location_id)


