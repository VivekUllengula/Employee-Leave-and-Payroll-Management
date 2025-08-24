from fastapi import APIRouter, HTTPException
from app.services import employee_service
from app.models.employee import EmployeeCreate
 
router = APIRouter(prefix="/employees", tags=["Employees"])
 
@router.post("/")
async def create_employee(employee: EmployeeCreate):
    new_employee = await employee_service.create_employee(employee.dict())
    if not new_employee:
        raise HTTPException(status_code=400, detail="Failed to create employee")
    return new_employee
 
