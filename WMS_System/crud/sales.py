from fastapi import HTTPException
from sqlalchemy import select, insert,func
from models import sales
from database import database
from schemas.sales import SaleCreate

async def generate_sale_number():
    query = select(func.count()).select_from(sales)
    count = await database.fetch_val(query)
    return f"SALE-{count + 1:05d}"

# CREATE SALE
async def create_sale(sale_data: SaleCreate):
    sale_dict = sale_data.dict(exclude={"lines"})

    # Agregar sale_number generado
    sale_dict["sale_number"] = await generate_sale_number()

    insert_query = insert(sales).values(**sale_dict)
    inserted_id = await database.execute(insert_query)

    return inserted_id

# GET SALE BY ID
async def get_sale_by_id(sale_id: int):
    query = select(sales).where(sales.c.id == sale_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Sale not found.")
    return result
