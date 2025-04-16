from models import item_class
from database import database
from schemas.ItemClass import ItemClassCreate
from fastapi import HTTPException

async def create_item_class(new_class: ItemClassCreate):
    query = item_class.select().where(item_class.c.item_class_id == new_class.item_class_id)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Item class already exists.")

    insert_query = item_class.insert().values(
        item_class_id=new_class.item_class_id,
        description=new_class.description
    )
    await database.execute(insert_query)
    return {"message": "Item class created successfully."}


async def get_all_item_classes():
    query = item_class.select()
    result = await database.fetch_all(query)

    return [
        {
            "id": row["id"],
            "item_class": row["item_class_id"],
            "description": row["description"]
        }
        for row in result
    ]

# UPDATE
async def update_item_class(item_class_id: int, updated_data: ItemClassCreate):
    query = item_class.update().where(item_class.c.id == item_class_id).values(
        item_class_id=updated_data.item_class_id,
        description=updated_data.description
    )
    await database.execute(query)
    return {"message": "Item class updated successfully."}

# DELETE
async def delete_item_class(item_class_id: int):
    query = item_class.delete().where(item_class.c.id == item_class_id)
    await database.execute(query)
    return {"message": "Item class deleted successfully."}
