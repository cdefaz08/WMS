from pydantic import BaseModel

class ItemClassCreate(BaseModel):
    item_class_id: str
    description: str