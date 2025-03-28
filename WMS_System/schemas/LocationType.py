from pydantic import BaseModel
from typing import Optional

class LocationTypeCreate(BaseModel):
    location_type: str
    description: Optional[str] = None
    system_flag: Optional[str] = "N"
    sto_pall_flag: Optional[str] = "N"
    sto_pall_cart_flag: Optional[str] = "N"
    sto_pall_con_flag: Optional[str] = "N"
    sto_cart_flag: Optional[str] = "N"
    sto_cont_flag: Optional[str] = "N"
    mix_item_flag: Optional[str] = "N"
    mix_cfg_flag: Optional[str] = "N"
    mix_trackingdate_flag: Optional[str] = "N"
    mix_receivingdate_flag: Optional[str] = "N"
    mix_recdate_flag: Optional[str] = "N"
    merge_flag: Optional[str] = "N"
    trash_pall: Optional[str] = "N"
    merge_cfg_code: Optional[str] = "N"
    merge_trackingdate: Optional[str] = "N"
    merge_inventory_type: Optional[str] = "N"
    merge_receiving_date: Optional[str] = "N"
    pick_pallet_flag: Optional[str] = "N"
    pick_cart_flag: Optional[str] = "N"
    pick_piece_flag: Optional[str] = "N"
