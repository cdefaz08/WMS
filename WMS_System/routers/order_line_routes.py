from fastapi import APIRouter
from typing import List
from crud import order_line_crud
from schemas.order_line import (
    OrderLine, OrderLineCreate, OrderLineUpdate
)

router = APIRouter(prefix="/order-lines", tags=["Order Lines"])


@router.post("/", response_model=OrderLine)
async def create_order_line(line_data: OrderLineCreate):
    return await order_line_crud.create_order_line(line_data)


@router.get("/", response_model=List[OrderLine])
async def get_all_order_lines():
    return await order_line_crud.get_order_lines()


@router.get("/{line_id}", response_model=OrderLine)
async def get_order_line_by_id(line_id: int):
    return await order_line_crud.get_order_line_by_id(line_id)


@router.get("/by-order/{order_id}", response_model=List[OrderLine])
async def get_lines_by_order(order_id: int):
    return await order_line_crud.get_lines_by_order_id(order_id)


@router.put("/{line_id}", response_model=OrderLine)
async def update_order_line(line_id: int, line_data: OrderLineUpdate):
    return await order_line_crud.update_order_line(line_id, line_data)


@router.delete("/{line_id}")
async def delete_order_line(line_id: int):
    return await order_line_crud.delete_order_line(line_id)
