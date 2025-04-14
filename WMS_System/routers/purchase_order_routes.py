from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from Security.dependencies import get_current_user
from crud import purchase_order_crud
from typing import Optional
from schemas.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderInDB
)

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
    dependencies=[Depends(get_current_user)]
)

# Create a new purchase order
@router.post("/", response_model=dict)
async def create_purchase_order(po: PurchaseOrderCreate,current_user= Depends(get_current_user)):
    created_by = current_user["username"]
    return await purchase_order_crud.create_purchase_order(po, created_by)


# Get all purchase orders
@router.get("/", response_model=List[PurchaseOrderInDB])
async def get_all_purchase_orders():
    return await purchase_order_crud.get_all_purchase_orders()

@router.get("/search", response_model=list[dict])
async def search_purchase_orders(
    po_number: Optional[str] = Query(None),
    vendor_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    return await purchase_order_crud.search_purchase_orders(
        po_number=po_number,
        vendor_code=vendor_code,
        status=status,
        start_date=start_date,
        end_date=end_date
    )


# Get purchase order by ID
@router.get("/{po_id}", response_model=PurchaseOrderInDB)
async def get_purchase_order(po_id: int):
    return await purchase_order_crud.get_purchase_order_by_id(po_id)


# Update purchase order
@router.put("/{po_id}", response_model=dict)
async def update_purchase_order(
    po_id: int,
    update_data: PurchaseOrderUpdate,
    current_user=Depends(get_current_user)
):
    modify_by = current_user["username"]
    return await purchase_order_crud.update_purchase_order(po_id, update_data, modify_by)


# Delete purchase order
@router.delete("/{po_id}", response_model=dict)
async def delete_purchase_order(po_id: int):
    return await purchase_order_crud.delete_purchase_order(po_id)
