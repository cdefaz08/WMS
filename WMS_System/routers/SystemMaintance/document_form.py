from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from schemas.SystemMaintance.document_form import DocumentForm, DocumentFormCreate, DocumentFormUpdate
import crud.SystemMaintance.document_form as crud

router = APIRouter(prefix="/document_forms", tags=["Document Forms"],
    dependencies=[Depends(get_current_user)])

@router.post("/", response_model=dict)
async def create(new_form: DocumentFormCreate):
    return await crud.create_document_form(new_form)

@router.get("/", response_model=list[DocumentForm])
async def get_all():
    return await crud.get_all_document_forms()

@router.get("/{form_id}", response_model=DocumentForm)
async def get_by_id(form_id: int):
    return await crud.get_document_form_by_id(form_id)

@router.put("/{form_id}")
async def update(form_id: int, updated: DocumentFormUpdate):
    return await crud.update_document_form(form_id, updated)

@router.delete("/{form_id}")
async def delete(form_id: int):
    return await crud.delete_document_form(form_id)
