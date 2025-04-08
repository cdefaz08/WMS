from fastapi import APIRouter, Depends
from database import database  # your async DB instance
import crud.proximity as crud
from schemas.proximity import ProximityCreate, Proximity

router = APIRouter(prefix="/proximities", tags=["Proximities"])

@router.post("/")
async def create(proximity: ProximityCreate):
    return await crud.create_proximity(database, proximity)

@router.get("/", response_model=list[Proximity])
async def read_all():
    return await crud.get_all_proximities(database)

@router.put("/{proximity_id}")
async def update(proximity_id: int, proximity: ProximityCreate):
    return await crud.update_proximity(database, proximity_id, proximity)

@router.delete("/{proximity_id}")
async def delete(proximity_id: int):
    return await crud.delete_proximity(database, proximity_id)

@router.get("/{proximity_id}", response_model=Proximity)
async def read_by_id(proximity_id: int):
    return await crud.get_proximity_by_id(database, proximity_id)

