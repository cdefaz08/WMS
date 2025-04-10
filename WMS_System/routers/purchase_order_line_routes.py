from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from typing import List
from crud import purchase_order_line_crud
from schemas.purchase_order_line import (
    PurchaseOrderLine, PurchaseOrderLineCreate, PurchaseOrderLineUpdate
)

router = APIRouter(prefix="/purchase-order-lines", tags=["Purchase Order Lines"],
    dependencies=[Depends(get_current_user)])


@router.post("/", response_model=PurchaseOrderLine)
async def create_po_line(line_data: PurchaseOrderLineCreate):
    return await purchase_order_line_crud.create_po_line(line_data)


@router.get("/", response_model=List[PurchaseOrderLine])
async def get_all_po_lines():
    return await purchase_order_line_crud.get_po_lines()


@router.get("/{line_id}", response_model=PurchaseOrderLine)
async def get_po_line_by_id(line_id: int):
    return await purchase_order_line_crud.get_po_line_by_id(line_id)


@router.get("/by-po/{po_id}", response_model=List[PurchaseOrderLine])
async def get_lines_by_po(po_id: int):
    return await purchase_order_line_crud.get_lines_by_po_id(po_id)


@router.put("/{line_id}", response_model=PurchaseOrderLine)
async def update_po_line(line_id: int, line_data: PurchaseOrderLineUpdate):
    return await purchase_order_line_crud.update_po_line(line_id, line_data)


@router.delete("/{line_id}")
async def delete_po_line(line_id: int):
    return await purchase_order_line_crud.delete_po_line(line_id)
