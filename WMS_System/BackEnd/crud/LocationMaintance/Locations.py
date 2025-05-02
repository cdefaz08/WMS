from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from models import locations
from database import database
from schemas.LocationMaintance.locations import LocationBase, LocationUpdate  # Asegúrate de importar correctamente
from typing import Optional

def convert_to_inches(value, uom):
    if value is None:
        return 0
    if not uom:
        return value  # Assume inches if UOM is missing
    uom = uom.lower()
    if uom == "feet":
        return value * 12
    elif uom == "cm":
        return value * 0.393701
    else:  # Assume inches
        return value


# Create with existence check
async def create_location(location: LocationBase):
    # Verificar si ya existe
    check_query = select(locations).where(locations.c.location_id == location.location_id)
    existing = await database.fetch_one(check_query)

    if existing:
        raise HTTPException(status_code=400, detail="Location with this ID already exists")

    location_data = location.dict()

    # Convert and calculate
    max_height_in = convert_to_inches(location_data.get("max_height"), location_data.get("uom_max_height"))
    max_width_in = convert_to_inches(location_data.get("max_width"), location_data.get("uom_max_width"))
    max_depth_in = convert_to_inches(location_data.get("max_depth"), location_data.get("uom_max_depth"))

    location_data["total_cubic_feet"] = (max_height_in * max_width_in * max_depth_in) / 1728 if (max_height_in and max_width_in and max_depth_in) else 0

    # Crear
    query = insert(locations).values(**location_data)
    await database.execute(query)
    return {**location_data, "location_id": location.location_id}


# Read All
async def get_all_locations():
    query = select(locations)
    return await database.fetch_all(query)


# Read by ID
async def get_location_by_id(location_id: str):
    query = select(locations).where(locations.c.location_id == location_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return result


async def update_location(location_id: str, location_data: LocationUpdate):
    update_data = location_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    if any(field in update_data for field in ["max_height", "max_width", "max_depth", "uom_max_height", "uom_max_width", "uom_max_depth"]):
        # Obtener valores actuales
        existing = await get_location_by_id(location_id)

        max_height = update_data.get("max_height", existing["max_height"])
        max_width = update_data.get("max_width", existing["max_width"])
        max_depth = update_data.get("max_depth", existing["max_depth"])

        uom_height = update_data.get("uom_max_height", existing["uom_max_height"])
        uom_width = update_data.get("uom_max_width", existing["uom_max_width"])
        uom_depth = update_data.get("uom_max_depth", existing["uom_max_depth"])

        max_height_in = convert_to_inches(max_height, uom_height)
        max_width_in = convert_to_inches(max_width, uom_width)
        max_depth_in = convert_to_inches(max_depth, uom_depth)

        update_data["total_cubic_feet"] = (max_height_in * max_width_in * max_depth_in) / 1728 if (max_height_in and max_width_in and max_depth_in) else 0

    query = (
        update(locations)
        .where(locations.c.location_id == location_id)
        .values(**update_data)
    )
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    return {**update_data, "location_id": location_id}


# Delete by ID
async def delete_location(location_id: str):
    query = delete(locations).where(locations.c.location_id == location_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}


#Filtrar por campos
async def search_locations(
    location_id: Optional[str] = None,
    aisle: Optional[str] = None,
    bay: Optional[str] = None,
    loc_level: Optional[str] = None,
    slot: Optional[str] = None,
    putaway_class: Optional[str] = None,
    rstk_class: Optional[str] = None,
    pick_class: Optional[str] = None,
    blocked_code: Optional[str] = None,
    location_type: Optional[str] = None,
    proximiti_in: Optional[str] = None,
    proximiti_out: Optional[str] = None
):
    query = select(locations)

    if location_id:
        query = query.where(locations.c.location_id.ilike(f"%{location_id}%"))
    if aisle:
        query = query.where(locations.c.aisle.ilike(f"%{aisle}%"))
    if bay:
        query = query.where(locations.c.bay.ilike(f"%{bay}%"))
    if loc_level:
        query = query.where(locations.c.loc_level.ilike(f"%{loc_level}%"))
    if slot:
        query = query.where(locations.c.slot.ilike(f"%{slot}%"))
    if putaway_class:
        query = query.where(locations.c.putaway_class.ilike(f"%{putaway_class}%"))
    if rstk_class:
        query = query.where(locations.c.rstk_class.ilike(f"%{rstk_class}%"))
    if pick_class:
        query = query.where(locations.c.pick_class.ilike(f"%{pick_class}%"))
    if blocked_code:
        query = query.where(locations.c.blocked_code.ilike(f"%{blocked_code}%"))
    if location_type:
        query = query.where(locations.c.location_type.ilike(f"%{location_type}%"))
    if proximiti_in:
        query = query.where(locations.c.proximiti_in.ilike(f"%{proximiti_in}%"))
    if proximiti_out:
        query = query.where(locations.c.proximiti_out.ilike(f"%{proximiti_out}%"))

    return await database.fetch_all(query)
