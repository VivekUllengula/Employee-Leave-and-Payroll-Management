from fastapi import APIRouter, HTTPException, Depends
from app.services import payroll_service
from app.models.payroll import PayrollCreate, PayrollUpdate, PayrollInDB
from app.utils.auth import get_current_user, role_checker

router = APIRouter(
    prefix="/payrolls",
    tags=["Payrolls"],
    dependencies=[Depends(get_current_user)]  
)

def not_found_or(data, message="Not found"):
    if not data:
        raise HTTPException(status_code=404, detail=message)
    return data

# Generate Payroll (admin/hr only)
@router.post("/generate/{employee_id}", response_model=PayrollInDB, dependencies=[Depends(role_checker(['admin', 'hr']))])
async def generate_payroll(employee_id: str, month: int, year: int):
    return not_found_or(
        await payroll_service.generate_payroll(employee_id, month, year),
        "Failed to generate payroll"
    )

# Get Payroll by ID
@router.get("/{payroll_id}", response_model=PayrollInDB)
async def get_payroll(payroll_id: str):
    return not_found_or(await payroll_service.get_payroll(payroll_id), "Payroll not found")

# Get All Payrolls
@router.get("/", response_model=list[PayrollInDB])
async def get_all_payrolls():
    return await payroll_service.get_all_payrolls()

# Update Payroll (admin/hr only)
@router.put("/{payroll_id}", response_model=PayrollInDB, dependencies=[Depends(role_checker(['admin', 'hr']))])
async def update_payroll(payroll_id: str, payroll: PayrollUpdate):
    return not_found_or(
        await payroll_service.update_payroll(payroll_id, payroll.dict(exclude_unset=True)),
        "Payroll not found or update failed"
    )

# Delete Payroll (admin/hr only)
@router.delete("/{payroll_id}", dependencies=[Depends(role_checker(['admin', 'hr']))])
async def delete_payroll(payroll_id: str):
    result = await payroll_service.delete_payroll(payroll_id)
    if not result.get("deleted"):
        raise HTTPException(status_code=404, detail="Payroll not found or already deleted")
    return {"message": "Payroll deleted successfully"}
