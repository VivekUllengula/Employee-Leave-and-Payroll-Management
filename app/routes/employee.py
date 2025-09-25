from fastapi import APIRouter, HTTPException, Depends
from app.services import employee_service
from app.models.employee import EmployeeCreate, EmployeeUpdate
from app.utils.auth import get_current_user, role_checker

router = APIRouter(prefix="/employees", tags=["Employees"], dependencies=[Depends(get_current_user)])

# Create a new employee 
@router.post("/", dependencies=[Depends(role_checker(['admin']))])
async def create_employee(employee: EmployeeCreate):
    #Create a new employee admin only
    new_employee = await employee_service.create_employee(employee.dict())
    if not new_employee:
        raise HTTPException(status_code=400, detail="Failed to create employee")
    return new_employee

# Get one employee by ID
@router.get("/{employee_id}")
async def get_employee(employee_id: str):
    employee = await employee_service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
 
# Get all employees
@router.get("/")
async def get_all_employees():
    return await employee_service.get_all_employees()

# Update employee
@router.put("/{employee_id}", dependencies=[Depends(role_checker(['admin', 'manager']))])
async def update_employee(employee_id: str, update_data: EmployeeUpdate):
    updated_employee = await employee_service.update_employee(
        employee_id, update_data.dict(exclude_unset=True)
    )
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found or update failed")
    return updated_employee
 
# Delete employee
@router.delete("/{employee_id}", dependencies=[Depends(role_checker(['admin']))])
async def delete_employee(employee_id: str):
    result = await employee_service.delete_employee(employee_id)
    if not result.get("deleted"):
        raise HTTPException(status_code=404, detail="Employee not found or already deleted")
    return {"message": "Employee deleted successfully"}
 
