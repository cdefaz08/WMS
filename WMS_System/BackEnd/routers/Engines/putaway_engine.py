# routes/putaway_engine.py

from fastapi import APIRouter, Depends
from fastapi import Query
from Security.dependencies import get_current_user
from schemas.Engines.putaway_engine import PalletInfo, PutawayResult
from crud.Engines.putaway_engine import calculate_putaway

router = APIRouter(
    prefix="/putaway",
    tags=["Putaway Engine"],
    dependencies=[Depends(get_current_user)]
)



@router.post("/calculate", response_model=PutawayResult)
async def calculate_putaway_endpoint(
    pallet: PalletInfo,
    rule_id: int = Query(..., description="Rule ID to use for putaway")
):
    result = await calculate_putaway(pallet, rule_id)
    return result
