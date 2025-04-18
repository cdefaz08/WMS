from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from schemas.SystemMaintance.label_form import LabelForm, LabelFormCreate, LabelFormUpdate
import crud.SystemMaintance.label_form as crud

router = APIRouter(prefix="/label_forms", tags=["Label Forms"],
    dependencies=[Depends(get_current_user)] )

@router.post("/", response_model=dict)
async def create(new_form: LabelFormCreate):
    return await crud.create_label_form(new_form)

@router.get("/", response_model=list[LabelForm])
async def get_all():
    return await crud.get_all_label_forms()

@router.get("/{form_id}", response_model=LabelForm)
async def get_by_id(form_id: int):
    return await crud.get_label_form_by_id(form_id)

@router.put("/{form_id}")
async def update(form_id: int, updated: LabelFormUpdate):
    return await crud.update_label_form(form_id, updated)

@router.delete("/{form_id}")
async def delete(form_id: int):
    return await crud.delete_label_form(form_id)
