from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PalletCreate(BaseModel):
    pallet_id: str
    location_id: str
    pallet_type: Optional[str] = None
    condition: Optional[str] = None
    adjust_reason: Optional[str] = None
    requester: Optional[str] = None
    created_date: datetime
    created_by: str

class PalletRead(BaseModel):
    id: int
    pallet_id: str
    location_id: str
    pallet_type: Optional[str] = None
    condition: Optional[str] = None
    adjust_reason: Optional[str] = None
    requester: Optional[str] = None
    created_date: datetime
    created_by: str

    class Config:
        from_attributes = True