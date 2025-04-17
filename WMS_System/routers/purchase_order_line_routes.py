from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Security.dependencies import get_current_user
from crud.purchase_order_line_crud import( create_purchase_order_line,
                                          get_all_purchase_order_lines,
                                          get_lines_by_po_id,
                                          get_purchase_order_line_by_id,
                                          update_purchase_order_line,
                                          delete_purchase_order_line
                                          )
from schemas.purchase_order_line import (
    PurchaseOrderLineCreate,
    PurchaseOrderLineUpdate,
    PurchaseOrderLineInDB
)

router = APIRouter(
    prefix="/purchase-order-lines",
    tags=["Purchase Order Lines"],
    dependencies=[Depends(get_current_user)]
)

# Create a new line
@router.post("/", response_model=dict)
async def create_po_line(
    line: PurchaseOrderLineCreate
):
    return await create_purchase_order_line(line)


# Get all lines
@router.get("/", response_model=List[PurchaseOrderLineInDB])
async def get_all_po_lines():
    return await get_all_purchase_order_lines()


# Get line by ID
@router.get("/{line_id}", response_model=PurchaseOrderLineInDB)
async def get_po_line(line_id: int):
    return await get_purchase_order_line_by_id(line_id)


# Get lines by purchase order ID
@router.get("/by-po/{po_id}", response_model=List[PurchaseOrderLineInDB])
async def get_po_lines_by_po_id(po_id: int):
    return await get_lines_by_po_id(po_id)


# Update a line
@router.put("/{line_id}", response_model=dict)
async def update_po_line(
    line_id: int,
    update_data: PurchaseOrderLineUpdate
):
    return await update_purchase_order_line(line_id, update_data)


# Delete a line
@router.delete("/{line_id}", response_model=dict)
async def delete_po_line(line_id: int):
    return await delete_purchase_order_line(line_id)
