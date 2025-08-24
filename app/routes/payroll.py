from fastapi import APIRouter, Depends, HTTPException
from app.db.mongo import get_db
from app.services import payroll_service, employee_service
 
router = APIRouter(prefix="/payroll", tags=["Payroll"])
 
 
@router.post("/generate/{employee_id}")
async def generate_payroll(employee_id: str, month: str, db=Depends(get_db)):
    employee = await employee_service.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await payroll_service.generate_monthly_payroll(db, employee, month)
 
 
@router.get("/{employee_id}")
async def get_payroll_history(employee_id: str, db=Depends(get_db)):
    return await payroll_service.get_payroll_history(db, employee_id)