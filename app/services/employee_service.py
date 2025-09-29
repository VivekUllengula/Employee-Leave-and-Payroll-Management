from bson import ObjectId
from app.db.mongo import get_db
from app.utils.mongo_helpers import convert_mongo_document, convert_many, normalize_document

# Create an employee 
async def create_employee(employee_data: dict):
    db = get_db() 
    employee_data = normalize_document(employee_data)
    result = await db["employees"].insert_one(employee_data)
    new_employee = await db["employees"].find_one({"_id": result.inserted_id})
    return convert_mongo_document(new_employee) if new_employee else None

#Create all employees in bulk
async def create_employees_bulk(employees_data: list):
    db = get_db()
    employees_data = [normalize_document(emp) for emp in employees_data]
    result = await db["employees"].insert_many(employees_data)
    new_employees = await db["employees"].find({"_id": {"$in": result.inserted_ids}}).to_list(len(result.inserted_ids))
    return convert_many(new_employees)

# Get one employee by ID
async def get_employee(employee_id: str):
    db = get_db()
    employee = await db["employees"].find_one({"_id": ObjectId(employee_id)})
    return convert_mongo_document(employee) if employee else None
 
# Get all employees (limit 100)
async def get_all_employees():
    db = get_db()
    employees = await db["employees"].find().to_list(100)
    return convert_many(employees)

# Update employee (normalize values before saving)
async def update_employee(employee_id: str, update_data: dict):
    db = get_db()
    update_data = normalize_document(update_data)  # convert dates if needed
    await db["employees"].update_one(
        {"_id": ObjectId(employee_id)}, {"$set": update_data}
    )
    updated = await db["employees"].find_one({"_id": ObjectId(employee_id)})
    return convert_mongo_document(updated) if updated else None
 
# Delete employee
async def delete_employee(employee_id: str):
    db = get_db()
    result = await db["employees"].delete_one({"_id": ObjectId(employee_id)})
    return {"deleted": result.deleted_count > 0}


