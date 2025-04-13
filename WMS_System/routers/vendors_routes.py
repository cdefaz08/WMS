from fastapi import APIRouter, Depends
from Security.dependencies import get_current_user
from typing import List
from crud import vendor
from schemas.vendor import Vendor, VendorCreate, VendorUpdate
from typing import Optional
from fastapi import Query
from crud.vendor import search_vendors

router = APIRouter(prefix="/vendors", tags=["Vendors"],
    dependencies=[Depends(get_current_user)])


@router.post("/", response_model=Vendor)
async def create_vendor(vendor_data: VendorCreate):
    return await vendor.create_vendor(vendor_data)



@router.get("/")
async def filter_vendors(
    vendor_code: Optional[str] = None,
    vendor_name: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    tax_id: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    zip_code: Optional[str] = None
):
    return await search_vendors(
        vendor_code=vendor_code,
        vendor_name=vendor_name,
        contact_name=contact_name,
        phone=phone,
        email=email,
        tax_id=tax_id,
        city=city,
        state=state,
        country=country,
        zip_code=zip_code
    )



@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor_by_id(vendor_id: int):
    return await vendor.get_vendor_by_id(vendor_id)


@router.put("/{vendor_id}", response_model=Vendor)
async def update_vendor(vendor_id: int, vendor_data: VendorUpdate):
    return await vendor.update_vendor(vendor_id, vendor_data)


@router.delete("/{vendor_id}", response_model=dict)
async def delete_vendor(vendor_id: int):
    deleted = await vendor.delete_vendor(vendor_id)
    return {"message": f"Vendor {deleted['vendor_code']} deleted."}
