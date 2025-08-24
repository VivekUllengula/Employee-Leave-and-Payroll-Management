from fastapi import HTTPException
from bson import ObjectId
 
 
async def create_employee(db, employee_data: dict) -> dict:

    """

    Insert a new employee into MongoDB.

    """

    res = await db.employees.insert_one(employee_data)

    return await db.employees.find_one({"_id": res.inserted_id})
 
 
async def get_employee(db, employee_id: str) -> dict:

    """

    Retrieve employee by ID.

    """

    employee = await db.employees.find_one({"_id": ObjectId(employee_id)})

    if not employee:

        raise HTTPException(status_code=404, detail="Employee not found")

    return employee
 
 
async def update_employee(db, employee_id: str, update_data: dict) -> dict:

    """

    Update employee details.

    """

    await db.employees.update_one({"_id": ObjectId(employee_id)}, {"$set": update_data})

    return await get_employee(db, employee_id)
 
 
async def delete_employee(db, employee_id: str) -> dict:

    """

    Delete employee.

    """

    res = await db.employees.delete_one({"_id": ObjectId(employee_id)})

    if res.deleted_count == 0:

        raise HTTPException(status_code=404, detail="Employee not found")

    return {"msg": "Employee deleted successfully"}

 