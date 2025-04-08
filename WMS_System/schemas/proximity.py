from pydantic import BaseModel

class ProximityBase(BaseModel):
    proximity: str
    movers: int = 0

class ProximityCreate(ProximityBase):
    pass

class Proximity(ProximityBase):
    id: int
