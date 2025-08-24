from fastapi import APIRouter, HTTPException
from app.services import payroll_service
from app.models.payroll import PayrollCreate, PayrollUpdate
 
router = APIRouter(prefix="/payrolls", tags=["Payrolls"])
 
# Generate Payroll
@router.post("/")
async def generate_payroll(payroll: PayrollCreate):
    new_payroll = await payroll_service.generate_payroll(payroll.dict())
    if not new_payroll:
        raise HTTPException(status_code=400, detail="Failed to generate payroll")
    return new_payroll
 
# Get Payroll by ID
@router.get("/{payroll_id}")
async def get_payroll(payroll_id: str):
    payroll = await payroll_service.get_payroll(payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return payroll
 
# Get All Payrolls
@router.get("/")
async def get_all_payrolls():
    return await payroll_service.get_all_payrolls()
 
# Update Payroll
@router.put("/{payroll_id}")
async def update_payroll(payroll_id: str, payroll: PayrollUpdate):
    updated_payroll = await payroll_service.update_payroll(payroll_id, payroll.dict(exclude_unset=True))
    if not updated_payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return updated_payroll
 
# Delete Payroll
@router.delete("/{payroll_id}")
async def delete_payroll(payroll_id: str):
    result = await payroll_service.delete_payroll(payroll_id)
    if not result["deleted"]:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return result