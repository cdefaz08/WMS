from fastapi import APIRouter, Body
from schemas.user import Users, UserUpdate
from crud import users as crud_users

router = APIRouter()

@router.post("/", response_model=dict)
async def create_user(user: Users):
    return await crud_users.create_user(user)

@router.get("/")
async def get_users():
    return await crud_users.get_users()

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    updated_data: UserUpdate = Body(...)
):
    return await crud_users.update_user(user_id,updated_data)

