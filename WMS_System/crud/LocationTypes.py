from fastapi import HTTPException
from sqlalchemy import insert
from models import location_types
from database import database  # Asegúrate de tener tu objeto `database`

#create Location Type
async def create_location_type(location_data):
    query = insert(location_types).values(**location_data.dict())
    try:
        await database.execute(query)
        return {"message": "Location type created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
