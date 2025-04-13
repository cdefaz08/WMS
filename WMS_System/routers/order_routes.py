from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from typing import List
from crud import order_crud
from schemas.order import Order, OrderCreate, OrderUpdate
from typing import Optional
from datetime import date
from fastapi import Query
from crud.order_crud import search_orders

router = APIRouter(prefix="/orders", tags=["Orders"],
    dependencies=[Depends(get_current_user)] )


@router.post("/", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user)  # 🔥 aquí accedemos al token decodificado
):
    return await order_crud.create_order(order_data, created_by=current_user["sub"])


@router.get("/")
async def search_orders_route(
    order_number: Optional[str] = None,
    customer_name: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[str] = None,
    document_form: Optional[str] = None,
    label_form: Optional[str] = None,
    order_type: Optional[str] = None,
    order_date_from: Optional[date] = Query(None, alias="order_date_from"),
    order_date_to: Optional[date] = Query(None, alias="order_date_to"),
    ship_date_from: Optional[date] = Query(None, alias="ship_date_from"),
    ship_date_to: Optional[date] = Query(None, alias="ship_date_to")
):
    return await search_orders(
        order_number=order_number,
        customer_name=customer_name,
        status=status,
        created_by=created_by,
        document_form=document_form,
        label_form=label_form,
        order_type=order_type,
        order_date_from=order_date_from,
        order_date_to=order_date_to,
        ship_date_from=ship_date_from,
        ship_date_to=ship_date_to
    )


@router.get("/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    return await order_crud.get_order_by_id(order_id)


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_data: OrderUpdate):
    return await order_crud.update_order(order_id, order_data)


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    return await order_crud.delete_order(order_id)
