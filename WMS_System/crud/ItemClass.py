
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
