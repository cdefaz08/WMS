from pydantic import BaseModel
from typing import Optional

# -------- Base schema reusable --------
class GroupBase(BaseModel):
    group_name: str
    description: Optional[str] = None

# -------- PUTAWAY GROUPS --------
class PutawayGroupCreate(GroupBase):
    pass

class PutawayGroupUpdate(BaseModel):
    description: Optional[str] = None

class PutawayGroupInDB(GroupBase):
    id: int

    class Config:
        from_attributes = True

# -------- PICK GROUPS --------
class PickGroupCreate(GroupBase):
    pass

class PickGroupUpdate(BaseModel):
    description: Optional[str] = None

class PickGroupInDB(GroupBase):
    id: int

    class Config:
        from_attributes = True

# -------- RESTOCK GROUPS --------
class RestockGroupCreate(GroupBase):
    pass

class RestockGroupUpdate(BaseModel):
    description: Optional[str] = None

class RestockGroupInDB(GroupBase):
    id: int

    class Config:
        from_attributes = True
