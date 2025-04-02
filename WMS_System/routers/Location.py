from fastapi import APIRouter, HTTPException
from typing import List

from schemas.locations import LocationBase, LocationUpdate
from crud.Locations import (
    create_location,
    get_all_locations,
    get_location_by_id,
    update_location,
    delete_location,
)

router = APIRouter()

# Create
@router.post("", response_model=LocationBase)
async def create_new_location(location: LocationBase):
    return await create_location(location)

# Read All
@router.get("", response_model=List[LocationBase])
async def read_all_locations():
    return await get_all_locations()

# Read by ID
@router.get("{location_id}", response_model=LocationBase)
async def read_location_by_id(location_id: str):
    return await get_location_by_id(location_id)

# Update by ID
@router.put("{location_id}", response_model=LocationUpdate)
async def update_location_by_id(location_id: str, location: LocationUpdate):
    return await update_location(location_id, location)

# Delete by ID
@router.delete("{location_id}")
async def delete_location_by_id(location_id: str):
    return await delete_location(location_id)
