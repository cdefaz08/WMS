from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
from database import database, metadata, engine
from models import items , users, item_class
from utils import Hash_password, verify_password
from typing import Optional

# Initialize FastAPI
app = FastAPI()

# Create database tables
metadata.create_all(engine)

class ItemClassCreate(BaseModel):
    item_class_id: str
    description: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Pydantic model for data validation
class Item(BaseModel):
    item_id: str
    description: str
    color: Optional[str] = None
    size: Optional[str] = None
    price: float
    upc: int
    item_class: Optional[str] = None
    alt_item_id1: Optional[int] = None
    alt_item_id2: Optional[int] = None
    description2: Optional[str] = None
    brand: Optional[str] = None
    style: Optional[str] = None
    is_offer: Optional[bool] = None
    default_cfg: Optional[str] = None
    custum1: Optional[str] = None
    custum2: Optional[str] = None
    custum3: Optional[str] = None
    custum4: Optional[str] = None
    custum5: Optional[str] = None
    custum6: Optional[str] = None


class Users(BaseModel):
    username: str
    password: str
    full_name: str
    max_logins: str
    email_addr: str
    pall_cap: float
    comments: str
    role : str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": await request.json()},
    )

# Start & stop database connection
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# CREATE - Add a new item
@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    if not item.item_id.strip():
        raise HTTPException(status_code=400, detail="item_id cannot be empty or null")
    
    if not item.description.strip():
        raise HTTPException(status_code=400, detail="description cannot be empty or null")        

    data = {
        "item_id": item.item_id,
        "description": item.description,
        "color": item.color,
        "size": item.size,
        "price": item.price,
        "upc": item.upc,
        "is_offer": item.is_offer,
        
    }

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


# READ - Get all items
@app.get("/items/")
async def read_items():
    query = items.select()
    return await database.fetch_all(query)

# READ - Get a specific item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE - Update an item by ID
@app.put("/items/{item_id}", response_model=dict)
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



# DELETE - Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item successfully deleted!"}

# Create User
@app.post("/Users/", response_model=dict)
async def create_user(user: Users):
    uppercase_username = user.username.upper()

   # Check if user already exists
    query = users.select().where(users.c.username == uppercase_username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and insert the user
    hash_password = Hash_password(user.password)
    query = users.insert().values(
        username=uppercase_username,
        password=hash_password,
        full_name= user.full_name,
        max_logins = user.max_logins,
        email_addr = user.email_addr,
        comments = user.comments,
        pall_cap = user.pall_cap,
        role=user.role
    )
    await database.execute(query)
    return {"message": "User successfully registered!"}

@app.get("/Users/")
async def get_users():
    query = users.select()
    result = await database.fetch_all(query)

    # Add 'user_id' key to ensure it's included in the response
    return [
        {
            "user_id": user["id"],  # Ensure the key matches what PyQt expects
            "username": user["username"],
            "password": user["password"],
            "role": user["role"]
        }
        for user in result
    ]

@app.delete("/Users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted!"}

@app.post("/login/")
async def login(request: LoginRequest):
    query = users.select().where(users.c.username == request.username)
    db_user = await database.fetch_one(query)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(request.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"message": "Login successful!"}


@app.put("/Users/{user_id}")
async def update_user(user_id: int, updated_data: dict):
    # Dictionary to hold only the provided data
    
    data_to_update = {}

    # Add username if provided
    if 'username' in updated_data and updated_data['username'].strip():
        data_to_update['username'] = updated_data['username'].upper()

    # Hash the password only if provided
    if 'password' in updated_data and updated_data['password'].strip():
        data_to_update['password'] = Hash_password(updated_data['password'])

    # Add role if provided
    if 'role' in updated_data and updated_data['role'].strip():
        data_to_update['role'] = updated_data['role']

    # If no valid data to update, return an error
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    # Perform the update only with the provided data
    query = users.update().where(users.c.id == user_id).values(data_to_update)
    result = await database.execute(query)

    if result:
        return {"message": "User updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Failed to update user")
    

@app.post("/item-classes/", response_model=dict)
async def create_item_class(new_class: ItemClassCreate):
    # Verificar si ya existe
    query = item_class.select().where(item_class.c.item_class_id == new_class.item_class_id)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Item class already exists.")

    insert_query = item_class.insert().values(
        item_class_id=new_class.item_class_id,
        description = new_class.description
        )
    await database.execute(insert_query)
    return {"message": "Item class created successfully."}


@app.get("/item-classes/")
async def get_item_classes():
    query = item_class.select()
    result = await database.fetch_all(query)
    return [{"id": row["id"], "item_class": row["item_class_id"], "description": row["description"]} for row in result]


