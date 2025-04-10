from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from typing import List
from crud import order_crud
from schemas.order import Order, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"],
    dependencies=[Depends(get_current_user)] )


@router.post("/", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user)  # 🔥 aquí accedemos al token decodificado
):
    return await order_crud.create_order(order_data, created_by=current_user["sub"])


@router.get("/", response_model=List[Order])
async def get_all_orders():
    return await order_crud.get_orders()


@router.get("/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    return await order_crud.get_order_by_id(order_id)


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_data: OrderUpdate):
    return await order_crud.update_order(order_id, order_data)


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    return await order_crud.delete_order(order_id)
