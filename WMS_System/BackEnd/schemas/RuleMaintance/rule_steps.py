from pydantic import BaseModel, Field
from typing import Optional


# ========================
# Putaway Rule Step Schemas
# ========================
class PutawayRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]= None
    putaway_to: Optional[str]= None
    putaway_group: Optional[str]= None
    location_type_from: Optional[str]= None
    location_type_to: Optional[str]= None
    UOM: Optional[str]= None
    min_percent: Optional[float] = Field(None, ge=0, le=100)
    max_percent: Optional[float] = Field(None, ge=0, le=100)
    sort_expresion: Optional[str]= None
    max_loc_Check: Optional[int]= None


class PutawayRuleStepCreate(PutawayRuleStepBase):
    pass


class PutawayRuleStepUpdate(BaseModel):
    seq: Optional[int] = None
    putaway_to: Optional[str]= None
    putaway_group: Optional[str]= None
    location_type_from: Optional[str]= None
    location_type_to: Optional[str]= None
    UOM: Optional[str]= None
    min_percent: Optional[float] = Field(None, ge=0, le=100)
    max_percent: Optional[float] = Field(None, ge=0, le=100)
    sort_expresion: Optional[str]= None
    max_loc_Check: Optional[int]= None


class PutawayRuleStep(PutawayRuleStepBase):
    id: int

    class Config:
        from_attributes = True


# ========================
# Pick Rule Step Schemas
# ========================
class PickRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]= None
    pick_group: Optional[str]= None
    pick_class: Optional[str]= None
    location_type: Optional[str]= None
    min_percent: Optional[float]= None
    max_percent: Optional[float]= None

class PickRuleStepCreate(PickRuleStepBase):
    pass

class PickRuleStepUpdate(BaseModel):
    seq: Optional[int]= None
    pick_group: Optional[str]= None
    pick_class: Optional[str]= None
    location_type: Optional[str]= None
    min_percent: Optional[float]= None
    max_percent: Optional[float]= None

class PickRuleStep(PickRuleStepBase):
    id: int

    class Config:
        from_attributes = True


# ========================
# Restock Rule Step Schemas
# ========================
class RestockRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]= None
    restock_group: Optional[str]= None
    restock_class: Optional[str]= None
    location_type: Optional[str]= None
    min_percent: Optional[float]= None
    max_percent: Optional[float]= None

class RestockRuleStepCreate(RestockRuleStepBase):
    pass

class RestockRuleStepUpdate(BaseModel):
    seq: Optional[int]= None
    restock_group: Optional[str]= None
    restock_class: Optional[str]= None
    location_type: Optional[str]= None
    min_percent: Optional[float]= None
    max_percent: Optional[float]= None

class RestockRuleStep(RestockRuleStepBase):
    id: int

    class Config:
        from_attributes = True
