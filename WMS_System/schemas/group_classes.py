from pydantic import BaseModel
from typing import Optional


# ---------------------
# PUTAWAY GROUP CLASSES
# ---------------------
class PutawayGroupClassBase(BaseModel):
    group_name: str
    class_name: str
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class PutawayGroupClassCreate(PutawayGroupClassBase):
    pass

class PutawayGroupClassUpdate(BaseModel):
    group_name: Optional[str] = None
    class_name: Optional[str] = None
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class PutawayGroupClassInDB(PutawayGroupClassBase):
    id: int

    class Config:
        from_attributes = True


# ------------------
# PICK GROUP CLASSES
# ------------------
class PickGroupClassBase(BaseModel):
    group_name: str
    class_name: str
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class PickGroupClassCreate(PickGroupClassBase):
    pass

class PickGroupClassUpdate(BaseModel):
    group_name: Optional[str] = None
    class_name: Optional[str] = None
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class PickGroupClassInDB(PickGroupClassBase):
    id: int

    class Config:
       from_attributes = True


# ---------------------
# RESTOCK GROUP CLASSES
# ---------------------
class RestockGroupClassBase(BaseModel):
    group_name: str
    class_name: str
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class RestockGroupClassCreate(RestockGroupClassBase):
    pass

class RestockGroupClassUpdate(BaseModel):
    group_name: Optional[str] = None
    class_name: Optional[str] = None
    priority: Optional[int] = None
    min_percent: Optional[float] = None
    max_percent: Optional[float] = None

class RestockGroupClassInDB(RestockGroupClassBase):
    id: int

    class Config:
        from_attributes = True
