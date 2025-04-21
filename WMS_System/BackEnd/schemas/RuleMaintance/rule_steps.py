from pydantic import BaseModel
from typing import Optional


# ========================
# Putaway Rule Step Schemas
# ========================
class PutawayRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]
    putaway_to: Optional[str]
    putaway_group: Optional[str]
    putaway_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class PutawayRuleStepCreate(PutawayRuleStepBase):
    pass

class PutawayRuleStepUpdate(BaseModel):
    seq: Optional[int]
    putaway_to: Optional[str]
    putaway_group: Optional[str]
    putaway_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class PutawayRuleStep(PutawayRuleStepBase):
    id: int

    class Config:
        from_attributes = True


# ========================
# Pick Rule Step Schemas
# ========================
class PickRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]
    pick_group: Optional[str]
    pick_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class PickRuleStepCreate(PickRuleStepBase):
    pass

class PickRuleStepUpdate(BaseModel):
    seq: Optional[int]
    pick_group: Optional[str]
    pick_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class PickRuleStep(PickRuleStepBase):
    id: int

    class Config:
        from_attributes = True


# ========================
# Restock Rule Step Schemas
# ========================
class RestockRuleStepBase(BaseModel):
    rule_id: int
    seq: Optional[int]
    restock_group: Optional[str]
    restock_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class RestockRuleStepCreate(RestockRuleStepBase):
    pass

class RestockRuleStepUpdate(BaseModel):
    seq: Optional[int]
    restock_group: Optional[str]
    restock_class: Optional[str]
    location_type: Optional[str]
    min_percent: Optional[float]
    max_percent: Optional[float]

class RestockRuleStep(RestockRuleStepBase):
    id: int

    class Config:
        from_attributes = True
