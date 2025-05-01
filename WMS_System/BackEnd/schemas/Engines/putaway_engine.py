# schemas/putaway_engine.py

from pydantic import BaseModel
from typing import Optional

class PalletInfo(BaseModel):
    pallet_id: str
    item_id: str
    item_uom: str
    total_quantity: float
    total_cubic: float
    total_weight: float
    location_type_from: Optional[str] = None

class PutawayResult(BaseModel):
    success: bool
    location_id: Optional[str] = None
    location_name: Optional[str] = None
    message: Optional[str] = None
