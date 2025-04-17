from fastapi import HTTPException
from sqlalchemy import select, insert
from models import sale_lines
from database import database
from schemas.sale_lines import SaleLineCreate
from typing import List


# BULK CREATE SALE LINES
async def create_sale_lines(sale_id: int, lines: List[SaleLineCreate]):
    line_dicts = [
        {**line.dict(), "sale_id": sale_id}
        for line in lines
    ]
    query = insert(sale_lines)
    await database.execute_many(query=query, values=line_dicts)


# GET LINES FOR A SALE
async def get_lines_by_sale_id(sale_id: int):
    query = select(sale_lines).where(sale_lines.c.sale_id == sale_id)
    return await database.fetch_all(query)
