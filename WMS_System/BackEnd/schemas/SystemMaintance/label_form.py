from pydantic import BaseModel
from typing import Optional

class LabelFormBase(BaseModel):
    label_form: str
    description: Optional[str] = None
    template_content: Optional[str] = None  # Aquí va la plantilla ZPL o texto

class LabelFormCreate(LabelFormBase):
    pass

class LabelFormUpdate(LabelFormBase):
    pass

class LabelForm(LabelFormBase):
    id: int

    class Config:
        from_attributes = True
