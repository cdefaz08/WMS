from fastapi import APIRouter
from typing import List
from crud import vendor
from schemas.vendor import Vendor, VendorCreate, VendorUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/", response_model=Vendor)
async def create_vendor(vendor_data: VendorCreate):
    return await vendor.create_vendor(vendor_data)


@router.get("/", response_model=List[Vendor])
async def get_all_vendors():
    return await vendor.get_vendors()


@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor_by_id(vendor_id: int):
    return await vendor.get_vendor_by_id(vendor_id)


@router.put("/{vendor_id}", response_model=Vendor)
async def update_vendor(vendor_id: int, vendor_data: VendorUpdate):
    return await vendor.update_vendor(vendor_id, vendor_data)


@router.delete("/{vendor_id}")
async def delete_vendor(vendor_id: int):
    return await vendor.delete_vendor(vendor_id)
