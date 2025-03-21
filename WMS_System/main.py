from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from database import database, metadata, engine
from models import items , users
from utils import Hash_password, verify_password

# Initialize FastAPI
app = FastAPI()

# Create database tables
metadata.create_all(engine)

class LoginRequest(BaseModel):
    username: str
    password: str

# Pydantic model for data validation
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class Users(BaseModel):
    username: str
    password: str
    role : str

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
    query = items.insert().values(
        name=item.name,
        price=item.price,
        is_offer=item.is_offer
    )
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
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    query = items.update().where(items.c.id == item_id).values(
        name=item.name,
        price=item.price,
        is_offer=item.is_offer
    )
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item successfully updated!"}

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

