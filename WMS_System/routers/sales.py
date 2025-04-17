from fastapi import APIRouter, Depends, HTTPException
from typing import List

from Security.dependencies import get_current_user
from schemas.sales import SaleCreate, Sale
from schemas.sale_lines import SaleLine
from crud import sales as sales_crud
from crud import sale_lines as lines_crud

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
    dependencies=[Depends(get_current_user)]
)


# ✅ Create Sale + Sale Lines
@router.post("/", response_model=Sale)
async def create_sale(new_sale: SaleCreate):
    # Save the main sale record
    sale_id = await sales_crud.create_sale(new_sale)

    # Save all lines (bulk insert)
    await lines_crud.create_sale_lines(sale_id, new_sale.lines)

    # Fetch full sale with lines
    sale_data = await sales_crud.get_sale_by_id(sale_id)
    lines_data = await lines_crud.get_lines_by_sale_id(sale_id)

    return {
        **sale_data,
        "lines": lines_data
    }


# ✅ Get Sale by ID
@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: int):
    sale_data = await sales_crud.get_sale_by_id(sale_id)
    lines_data = await lines_crud.get_lines_by_sale_id(sale_id)

    return {
        **sale_data,
        "lines": lines_data
    }
