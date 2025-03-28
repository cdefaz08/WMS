from fastapi import APIRouter
from schemas.LocationType import LocationTypeCreate , LocationTypeUpdate
from crud.LocationTypes import create_location_type , get_all_location_types , update_location_type , delete_location_type, get_location_type_by_id

router = APIRouter()

@router.post("")
async def add_location_type(location_type: LocationTypeCreate):
    return await create_location_type(location_type)

@router.get("")
async def get_location_types():
    return await get_all_location_types()

@router.put("/{location_type}")
async def put_location_type(location_type: str, update_data: LocationTypeUpdate):
    return await update_location_type(location_type, update_data)

@router.get("/{location_type}")
async def get_location_type(location_type: str):
    return await get_location_type_by_id(location_type)

@router.delete("/{location_type}")
async def remove_location_type(location_type: str):
    return await delete_location_type(location_type)