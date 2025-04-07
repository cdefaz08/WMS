from fastapi import APIRouter
from typing import List
from crud import purchase_order_crud
from schemas.purchase_order import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


@router.post("/", response_model=PurchaseOrder)
async def create_po(po_data: PurchaseOrderCreate):
    return await purchase_order_crud.create_purchase_order(po_data)


@router.get("/", response_model=List[PurchaseOrder])
async def get_all_pos():
    return await purchase_order_crud.get_purchase_orders()


@router.get("/{po_id}", response_model=PurchaseOrder)
async def get_po_by_id(po_id: int):
    return await purchase_order_crud.get_purchase_order_by_id(po_id)


@router.put("/{po_id}", response_model=PurchaseOrder)
async def update_po(po_id: int, po_data: PurchaseOrderUpdate):
    return await purchase_order_crud.update_purchase_order(po_id, po_data)


@router.delete("/{po_id}")
async def delete_po(po_id: int):
    return await purchase_order_crud.delete_purchase_order(po_id)
