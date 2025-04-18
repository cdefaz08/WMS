from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    location_id: str
    location_type: Optional[str] = None
    scan_location: str
    black_hole_flag: Optional[str] = None
    proximiti_in: Optional[str] = None
    proximiti_out: Optional[str] = None
    has_assign_flag :Optional[str] = None
    has_contents_flag : Optional[str] = None
    has_pending_flag : Optional[str] = None
    putaway_class : str
    pick_class : str
    rstk_class : str
    blocked_code : Optional[str] = None
    palle_cap : Optional[int] = None
    carton_cap : Optional[int] = None
    max_weight : Optional[float] = None
    max_height : Optional[float] = None
    max_width : Optional[float] = None
    max_depth : Optional[float] = None
    uom_max_weight : Optional[str] = None
    uom_max_height : Optional[str] = None
    uom_max_width : Optional[str] = None
    uom_max_depth : Optional[str] = None
    uom_carton_cap : Optional[str] = None
    pallet_qty_act : Optional[int] = None
    carton_qty_act : Optional[int] = None
    aisle : Optional[str] = None
    bay : Optional[str] = None
    loc_level : Optional[str] = None
    slot : Optional[str] = None
    pnd_location_id1 : Optional[str] = None
    pnd_location_id2 : Optional[str] = None
    last_touch: Optional[datetime] = None


class LocationUpdate(BaseModel):
    location_id: Optional[str] = None
    location_type: Optional[str] = None
    scan_location: Optional[str] = None
    black_hole_flag: Optional[str] = None
    proximiti_in: Optional[str] = None
    proximiti_out: Optional[str] = None
    has_assign_flag :Optional[str] = None
    has_contents_flag : Optional[str] = None
    has_pending_flag : Optional[str] = None
    putaway_class : Optional[str] = None
    pick_class : Optional[str] = None
    rstk_class : Optional[str] = None
    blocked_code : Optional[str] = None
    palle_cap : Optional[int] = None
    carton_cap : Optional[int] = None
    max_weight : Optional[float] = None
    max_height : Optional[float] = None
    max_width : Optional[float] = None
    max_depth : Optional[float] = None
    uom_max_weight : Optional[str] = None
    uom_max_height : Optional[str] = None
    uom_max_width : Optional[str] = None
    uom_max_depth : Optional[str] = None
    uom_carton_cap : Optional[str] = None
    pallet_qty_act : Optional[int] = None
    carton_qty_act : Optional[int] = None
    aisle : Optional[str] = None
    bay : Optional[str] = None
    loc_level : Optional[str] = None
    slot : Optional[str] = None
    pnd_location_id1 : Optional[str] = None
    pnd_location_id2 : Optional[str] = None
    last_touch: Optional[datetime] = None