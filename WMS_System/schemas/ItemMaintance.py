from pydantic import BaseModel
from typing import Optional

class ItemMaintanceBase(BaseModel):
    item_id: int
    is_default: Optional[bool] = False

    # Dimensiones
    pallet_length: Optional[float]= None
    pallet_width: Optional[float]= None
    pallet_height: Optional[float]= None

    case_length: Optional[float]= None
    case_width: Optional[float]= None
    case_height: Optional[float]= None

    piece_length: Optional[float]= None
    piece_width: Optional[float]= None
    piece_height: Optional[float]= None

    inner_length: Optional[float]= None
    inner_width: Optional[float]= None
    inner_height: Optional[float]= None

    # Pesos
    pallet_weight: Optional[float]= None
    case_weight: Optional[float]= None
    piece_weight: Optional[float]= None
    inner_weight: Optional[float]= None

    # Cantidades por unidad
    boxes_per_pallet: Optional[int]= None
    pieces_per_case: Optional[int]= None
    inners_per_piece: Optional[int]= None

    # UOM y códigos de barra
    unit_of_measure: Optional[str]= None
    barcode_case: Optional[str]= None
    barcode_pallet: Optional[str]= None
    barcode_inner: Optional[str]= None

    # Información adicional
    configuration_name: Optional[str]= None
    notes: Optional[str]= None

class ItemMaintanceCreate(ItemMaintanceBase):
    pass

class ItemMaintanceUpdate(ItemMaintanceBase):
    pass

class ItemMaintance(ItemMaintanceBase):
    id: int

    class Config:
        from_attributes = True
