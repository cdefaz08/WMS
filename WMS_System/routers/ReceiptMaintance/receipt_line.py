from fastapi import APIRouter, HTTPException, Depends
from Security.dependencies import get_current_user
from schemas.ReceiptMaintance.receipt_line_schema import ReceiptLineCreate, ReceiptLine
import crud.ReceiptMaintance.receipt_line as receipt_line_crud

router = APIRouter(
    prefix="/receipt-lines",
    tags=["Receipt Lines"],
    dependencies=[Depends(get_current_user)]
)


# 🔹 Crear una nueva línea de recibo
@router.post("/", response_model=dict)
async def create_receipt_line_endpoint(receipt_line: ReceiptLineCreate):
    return await receipt_line_crud.create_receipt_line(receipt_line)


# 🔹 Obtener todas las líneas
@router.get("/", response_model=list[ReceiptLine])
async def get_all_receipt_lines_endpoint():
    return await receipt_line_crud.get_all_receipt_lines()


# 🔹 Obtener línea por ID
@router.get("/id/{line_id}", response_model=ReceiptLine)
async def get_receipt_line_by_id_endpoint(line_id: int):
    return await receipt_line_crud.get_receipt_line_by_id(line_id)


# 🔹 Obtener líneas por receipt_number
@router.get("/receipt/{receipt_number}", response_model=list[ReceiptLine])
async def get_receipt_lines_by_receipt_number_endpoint(receipt_number: str):
    return await receipt_line_crud.get_receipt_lines_by_receipt_number(receipt_number)


# 🔹 Actualizar una línea
@router.put("/{line_id}", response_model=dict)
async def update_receipt_line_endpoint(line_id: int, updated_data: dict):
    return await receipt_line_crud.update_receipt_line(line_id, updated_data)


# 🔹 Eliminar una línea
@router.delete("/{line_id}", response_model=dict)
async def delete_receipt_line_endpoint(line_id: int):
    return await receipt_line_crud.delete_receipt_line(line_id)
