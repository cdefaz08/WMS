from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared base schema
class AContentsBase(BaseModel):
    location_id: int
    pallet_id: Optional[int] = None
    item_code: str
    pieces_on_hand: int = 0
    receipt_info: Optional[str] = None
    receipt_release_num: Optional[str] = None
    date_time_last_touched: datetime
    user_last_touched: str

# Schema for creation (input)
class AContentsCreate(AContentsBase):
    pass

# Schema for update (input)
class AContentsUpdate(BaseModel):
    location_id: Optional[int] = None
    pallet_id: Optional[int] = None
    item_code: Optional[str] = None
    pieces_on_hand: Optional[int] = None
    receipt_info: Optional[str] = None
    receipt_release_num: Optional[str] = None
    date_time_last_touched: Optional[datetime] = None
    user_last_touched: Optional[str] = None

# Schema for reading (output)
class AContentsOut(AContentsBase):
    id: int

    class Config:
        orm_mode = True
