from database import database
from sqlalchemy import select
from models import items
from schemas.Items import ItemCreate
from fastapi import HTTPException

#Create Item
async def create_item(item: ItemCreate):
    if not item.item_id.strip():
        raise HTTPException(status_code=400, detail="item_id cannot be empty or null")
    
    if not item.description.strip():
        raise HTTPException(status_code=400, detail="description cannot be empty or null")        

    data = {
        "item_id": item.item_id,
        "description": item.description,
        "price": item.price,
        "upc": item.upc,
        "is_offer": item.is_offer,
        
    }

    if item.upc:
        data["upc"] = item.upc

    if item.color.strip():
        data["color"] = item.color
    
    if item.size.strip():
        data["size"] = item.size

    if item.description2.strip():
        data["description2"]= item.description2

    if item.alt_item_id1:
        data["alt_item_id1"] = item.alt_item_id1

    if item.alt_item_id2:
        data["alt_item_id2"] = item.alt_item_id2

    if item.brand.strip():
        data["brand"]= item.brand
    if item.style.strip():
        data["style"] = item.style

    if item.custum1.strip():
        data["custum1"] = item.custum1
    if item.custum2.strip():
        data["custum2"] = item.custum2
    if item.custum3.strip():
        data["custum3"] = item.custum3
    if item.custum4.strip():
        data["custum4"] = item.custum4
    if item.custum5.strip():
        data["custum5"] = item.custum5
    if item.custum6.strip():
        data["custum6"] = item.custum6

    # ✅ Solo agregar item_class si está presente
    if item.item_class.strip():
        data["item_class"] = item.item_class
    else:
        data["item_class"] = 'STND'
        # ✅ If default_cfg is not provided or is blank, set it to None

    if item.default_cfg and item.default_cfg.strip():
        data["default_cfg"] = item.default_cfg
    else:
        data["default_cfg"] = None  # Will insert NULL into the database

    # ✅ Ahora puedes insertar el diccionario en la consulta
    query = items.insert().values(**data)

    await database.execute(query)
    return {"message": "Item successfully added!"}

# Read all Items
async def read_items():
    query = items.select()
    return await database.fetch_all(query)

#Read selecte Item
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

#update Item by Item id
async def update_item(item_id: int, updated_data: dict):
    data_to_update = {}

    for key, value in updated_data.items():
        # Convert string prices to float
        if key == "price":
            try:
                data_to_update[key] = float(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Price must be a number")
        else:
            data_to_update[key] = value

    if not data_to_update:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    query = items.update().where(items.c.id == item_id).values(data_to_update)
    result = await database.execute(query)

    if result:
        return {"message": "Item updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Failed to update item")
#Delete Item by Item id
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item successfully deleted!"}

async def get_item_by_upc(upc: int):
    query = select(items).where(items.c.upc == upc)
    item = await database.fetch_one(query)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item
    
async def search_items(
    item_id=None,
    upc=None,
    alt_item_id1=None,
    alt_item_id2=None,
    item_class=None,
    color=None,
    size=None,
    brand=None
):
    query = items.select()

    # Apply filters dynamically
    if item_id:
        query = query.where(items.c.item_id.ilike(f"%{item_id}%"))
    if upc:
        query = query.where(items.c.upc.ilike(f"%{upc}%"))
    if alt_item_id1:
        query = query.where(items.c.alt_item_id1.ilike(f"%{alt_item_id1}%"))
    if alt_item_id2:
        query = query.where(items.c.alt_item_id2.ilike(f"%{alt_item_id2}%"))
    if item_class:
        query = query.where(items.c.item_class.ilike(f"%{item_class}%"))
    if color:
        query = query.where(items.c.color.ilike(f"%{color}%"))
    if size:
        query = query.where(items.c.size.ilike(f"%{size}%"))
    if brand:
        query = query.where(items.c.brand.ilike(f"%{brand}%"))

    return await database.fetch_all(query)
