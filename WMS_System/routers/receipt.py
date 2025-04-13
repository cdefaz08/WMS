from fastapi import APIRouter, HTTPException ,Depends
from Security.dependencies import get_current_user
from schemas.receipt_schema import ReceiptCreate, Receipt
import crud.receipt as receipt_crud
from typing import Optional
from fastapi import Query
from datetime import date
from crud.receipt import search_receipts

router = APIRouter(prefix="/receipts", tags=["Receipts"],
    dependencies=[Depends(get_current_user)])


# 🔹 Crear un nuevo recibo
@router.post("/", response_model=dict)
async def create_receipt_endpoint(
    receipt: ReceiptCreate,
    current_user: dict = Depends(get_current_user)
):
    return await receipt_crud.create_receipt(receipt, created_by=current_user["sub"])


@router.get("/")
async def search_receipts_route(
    receipt_number: Optional[str] = None,
    release_num: Optional[str] = None,
    vendor_name: Optional[str] = None,
    invoice_num: Optional[str] = None,
    po_id: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[str] = None,
    expected_from: Optional[date] = Query(None, alias="expected_from"),
    expected_to: Optional[date] = Query(None, alias="expected_to"),
    received_from: Optional[date] = Query(None, alias="received_from"),
    received_to: Optional[date] = Query(None, alias="received_to"),
):
    return await search_receipts(
        receipt_number=receipt_number,
        release_num=release_num,
        vendor_name=vendor_name,
        invoice_num=invoice_num,
        po_id=po_id,
        status=status,
        created_by=created_by,
        expected_from=expected_from,
        expected_to=expected_to,
        received_from=received_from,
        received_to=received_to,
    )



# 🔹 Obtener recibo por ID
@router.get("/{receipt_id}", response_model=Receipt)
async def get_receipt_by_id_endpoint(receipt_id: int):
    return await receipt_crud.get_receipt_by_id(receipt_id)



# 🔹 Obtener recibo por número
@router.get("/number/{receipt_number}", response_model=Receipt)
async def get_receipt_by_number_endpoint(receipt_number: str):
    return await receipt_crud.get_receipt_by_number(receipt_number)


# 🔹 Actualizar un recibo
@router.put("/{receipt_id}", response_model=dict)
async def update_receipt_endpoint(receipt_id: int, updated_data: dict):
    return await receipt_crud.update_receipt(receipt_id, updated_data)


# 🔹 Eliminar un recibo
@router.delete("/{receipt_id}", response_model=dict)
async def delete_receipt_endpoint(receipt_id: int):
    return await receipt_crud.delete_receipt(receipt_id)
