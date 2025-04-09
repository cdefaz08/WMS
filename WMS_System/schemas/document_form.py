from pydantic import BaseModel
from typing import Optional

class DocumentFormBase(BaseModel):
    document_form: str
    description: Optional[str] = None
    template_content: Optional[str] = None  # Aquí se guarda el ZPL

class DocumentFormCreate(DocumentFormBase):
    pass

class DocumentFormUpdate(DocumentFormBase):
    pass

class DocumentForm(DocumentFormBase):
    id: int

    class Config:
        from_attributes = True
