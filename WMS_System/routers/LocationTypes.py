from fastapi import APIRouter
from schemas.LocationType import LocationTypeCreate
from crud.LocationTypes import create_location_type

router = APIRouter()

@router.post("")
async def add_location_type(location_type: LocationTypeCreate):
    return await create_location_type(location_type)
