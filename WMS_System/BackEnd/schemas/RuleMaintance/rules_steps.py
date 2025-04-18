from pydantic import BaseModel
from typing import Optional


# -------- PUTAWAY RULES --------
class PutawayRuleBase(BaseModel):
    rule_name: str
    description: Optional[str] = None
    priority: Optional[int] = None

class PutawayRuleCreate(PutawayRuleBase):
    pass

class PutawayRuleUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None

class PutawayRuleOut(PutawayRuleBase):
    id: int

    class Config:
        from_attributes = True


# -------- PICK RULES --------
class PickRuleBase(BaseModel):
    rule_name: str
    description: Optional[str] = None
    priority: Optional[int] = None

class PickRuleCreate(PickRuleBase):
    pass

class PickRuleUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None

class PickRuleOut(PickRuleBase):
    id: int

    class Config:
        from_attributes = True


# -------- RESTOCK RULES --------
class RestockRuleBase(BaseModel):
    rule_name: str
    description: Optional[str] = None
    priority: Optional[int] = None

class RestockRuleCreate(RestockRuleBase):
    pass

class RestockRuleUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None

class RestockRuleOut(RestockRuleBase):
    id: int

    class Config:
        from_attributes = True