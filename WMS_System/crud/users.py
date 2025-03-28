from models import users
from utils import Hash_password
from database import database
from fastapi import HTTPException
from schemas.user import UserUpdate , Users

#--------------Create User------------------#
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

#Get all the Users
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

#Delete user by User_id
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted!"}

#Update User data
async def update_user(user_id: int, updated_data: UserUpdate):
    data_to_update = {}

    if updated_data.username and updated_data.username.strip():
        data_to_update['username'] = updated_data.username.upper()

    if updated_data.password and updated_data.password.strip():
        data_to_update['password'] = Hash_password(updated_data.password)

    if updated_data.role and updated_data.role.strip():
        data_to_update['role'] = updated_data.role

    if updated_data.full_name and updated_data.full_name.strip():
        data_to_update['full_name'] = updated_data.full_name

    if updated_data.email_addr and updated_data.email_addr.strip():
        data_to_update['email_addr'] = updated_data.email_addr

    if updated_data.max_logins is not None:
        data_to_update['max_logins'] = updated_data.max_logins

    if updated_data.pall_cap is not None:
        data_to_update['pall_cap'] = updated_data.pall_cap

    if updated_data.comments is not None:
        data_to_update['comments'] = updated_data.comments

    if not data_to_update:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    query = users.update().where(users.c.id == user_id).values(data_to_update)
    result = await database.execute(query)

    if result:
        return {"message": "User updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Failed to update user")




