from pydantic import BaseModel
from typing import Optional

class RestockClassBase(BaseModel):
    class_name: str
    description: str

class RestockClassCreate(RestockClassBase):
    pass

class RestockClassUpdate(BaseModel):
    class_name: Optional[str] = None
    description: Optional[str] = None

class RestockClass(RestockClassBase):
    id: int
    class Config:
        model_config = {"from_attributes": True}



class PutawayClassBase(BaseModel):
    class_name : str
    description: str

class PutawayClassCreate(PutawayClassBase):
    pass

class PutawayClassUpdate(BaseModel):
    class_name: Optional[str] = None
    description: Optional[str] = None

class PutawayClass(PutawayClassBase):
    id : int
    class Config:
        model_config = {"from_attributes": True}



class PickClasesBase(BaseModel):
    class_name : str
    description: str

class PickClassCreate(PickClasesBase):
    pass

class PickClassUpdate(BaseModel):
    class_name : Optional[str]
    description : Optional[str]

class PickClass(PickClasesBase):
    id : int
    class Config:
        model_config = {"from_attributes": True}


 