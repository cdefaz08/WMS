from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import Doc_form
from schemas.SystemMaintance.document_form import DocumentFormCreate, DocumentFormUpdate
from database import database

# CREATE
async def create_document_form(new_form: DocumentFormCreate):
    query = select(Doc_form).where(Doc_form.c.document_form == new_form.document_form)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Document form already exists.")

    insert_query = insert(Doc_form).values(**new_form.dict())
    inserted_id = await database.execute(insert_query)
    return { "id": inserted_id, "message": "Document form created successfully." }

# GET ALL
async def get_all_document_forms():
    query = select(Doc_form)
    return await database.fetch_all(query)

# GET BY ID
async def get_document_form_by_id(form_id: int):
    query = select(Doc_form).where(Doc_form.c.id == form_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Document form not found.")
    return result

# UPDATE
async def update_document_form(form_id: int, updated_data: DocumentFormUpdate):
    query = select(Doc_form).where(Doc_form.c.id == form_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Document form not found.")

    update_query = update(Doc_form).where(Doc_form.c.id == form_id).values(**updated_data.dict(exclude_unset=True))
    await database.execute(update_query)
    return { "message": "Document form updated successfully." }

# DELETE
async def delete_document_form(form_id: int):
    query = select(Doc_form).where(Doc_form.c.id == form_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Document form not found.")

    delete_query = delete(Doc_form).where(Doc_form.c.id == form_id)
    await database.execute(delete_query)
    return { "message": "Document form deleted successfully." }
