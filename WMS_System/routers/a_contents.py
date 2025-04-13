from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from typing import List
from schemas.a_contents import AContentsCreate, AContentsUpdate, AContentsOut
from crud import a_contents as crud
from fastapi import HTTPException
from typing import Optional

router = APIRouter(prefix="/a-contents", tags=["A_Contents"],
    dependencies=[Depends(get_current_user)])

# CREATE
@router.post("/", response_model=dict)
async def create_a_content(entry: AContentsCreate):
    return await crud.create_a_content(entry)

# GET ALL
@router.get("/", response_model=List[AContentsOut])
async def get_all_contents():
    return await crud.get_all_a_contents()

# GET BY ID
@router.get("/{content_id}", response_model=AContentsOut)
async def get_content_by_id(content_id: int):
    return await crud.get_a_content_by_id(content_id)

# UPDATE
@router.put("/{content_id}", response_model=dict)
async def update_content(content_id: int, updated: AContentsUpdate):
    return await crud.update_a_content(content_id, updated)

# DELETE
@router.delete("/{content_id}", response_model=dict)
async def delete_content(content_id: int):
    return await crud.delete_a_content(content_id)

@router.get("/", response_model=List[AContentsOut])
async def get_filtered_contents(
    location_id: Optional[str] = None,
    pallet_id: Optional[str] = None,
    item_code: Optional[str] = None,
    receipt_info: Optional[str] = None,
    receipt_release_num: Optional[str] = None,
):
    return await crud.get_filtered_a_contents(
        location_id=location_id,
        pallet_id=pallet_id,
        item_code=item_code,
        receipt_info=receipt_info,
        receipt_release_num=receipt_release_num
    )
