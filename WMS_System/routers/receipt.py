from fastapi import APIRouter, HTTPException ,Depends
from Security.dependencies import get_current_user
from schemas.receipt_schema import ReceiptCreate, Receipt
import crud.receipt as receipt_crud

router = APIRouter(prefix="/receipts", tags=["Receipts"],
    dependencies=[Depends(get_current_user)])


# 🔹 Crear un nuevo recibo
@router.post("/", response_model=dict)
async def create_receipt_endpoint(receipt: ReceiptCreate):
    return await receipt_crud.create_receipt(receipt)


# 🔹 Obtener todos los recibos
@router.get("/", response_model=list[Receipt])
async def get_all_receipts_endpoint():
    return await receipt_crud.get_all_receipts()


# 🔹 Obtener recibo por ID
@router.get("/id/{receipt_id}", response_model=Receipt)
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
