from fastapi import APIRouter, HTTPException, Depends
from Security.dependencies import get_current_user
from sqlalchemy import select
from models import pallets
from database import database
from schemas.ItemMaintace.Pallets import PalletCreate, PalletRead
from datetime import datetime
from crud.ItemMaintance.pallets import (
    create_pallet,
    get_all_pallets,
    get_pallet_by_id,
    update_pallet,
    delete_pallet,
)

router = APIRouter(
    prefix="/pallets",
    tags=["Pallets"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=dict)
async def create_pallet_route(
    pallet_data: PalletCreate,
    current_user: dict = Depends(get_current_user),   # 🛡️ get user from token
):
    # ➡️ Here we inject automatically the user and date
    pallet_data_dict = pallet_data.dict()
    pallet_data_dict["created_by"] = current_user["id"]  # 🛡️ Auto set
    pallet_data_dict["created_date"] = datetime.now().isoformat()

    return await create_pallet(pallet_data_dict)

# GET ALL
@router.get("/", response_model=list[PalletRead])
async def list_all_pallets():
    return await get_all_pallets()

@router.get("/by-location/{location_id}")
async def get_pallets_by_location(location_id: str):
    query = select(pallets).where(pallets.c.location_id == location_id)
    pallets_at_location = await database.fetch_all(query)

    if not pallets_at_location:
        return []  # No pallets found

    return pallets_at_location

# GET BY ID
@router.get("/{pallet_id}", response_model=PalletRead)
async def get_pallet(pallet_id: str):
    return await get_pallet_by_id(pallet_id)

# UPDATE
@router.put("/{pallet_id}", response_model=dict)
async def update_existing_pallet(pallet_id: str, entry: PalletCreate):
    return await update_pallet(pallet_id, entry)

# DELETE
@router.delete("/{pallet_id}", response_model=dict)
async def delete_existing_pallet(pallet_id: str):
    return await delete_pallet(pallet_id)
