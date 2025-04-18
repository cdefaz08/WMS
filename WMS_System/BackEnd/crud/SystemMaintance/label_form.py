from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from models import Label_form
from schemas.SystemMaintance.label_form import LabelFormCreate, LabelFormUpdate
from database import database

# CREATE
async def create_label_form(new_form: LabelFormCreate):
    query = select(Label_form).where(Label_form.c.label_form == new_form.label_form)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Label form already exists.")

    insert_query = insert(Label_form).values(**new_form.dict())
    inserted_id = await database.execute(insert_query)
    return { "id": inserted_id, "message": "Label form created successfully." }

# GET ALL
async def get_all_label_forms():
    query = select(Label_form)
    return await database.fetch_all(query)

# GET BY ID
async def get_label_form_by_id(form_id: int):
    query = select(Label_form).where(Label_form.c.id == form_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Label form not found.")
    return result

# UPDATE
async def update_label_form(form_id: int, updated_data: LabelFormUpdate):
    query = select(Label_form).where(Label_form.c.id == form_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Label form not found.")

    update_query = update(Label_form).where(Label_form.c.id == form_id).values(**updated_data.dict(exclude_unset=True))
    await database.execute(update_query)
    return { "message": "Label form updated successfully." }

# DELETE
async def delete_label_form(form_id: int):
    query = select(Label_form).where(Label_form.c.id == form_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Label form not found.")

    delete_query = delete(Label_form).where(Label_form.c.id == form_id)
    await database.execute(delete_query)
    return { "message": "Label form deleted successfully." }
