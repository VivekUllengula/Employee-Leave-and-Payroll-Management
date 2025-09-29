from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db
from app.utils.mongo_helpers import convert_mongo_document, convert_many, normalize_document
from app.models.leave import LeaveStatus

async def create_leave(leave_data: dict):
    db = get_db()
    leave_data = normalize_document(leave_data)
    leave_data["status"] = LeaveStatus.PENDING
    leave_data["requested_on"] = datetime.utcnow()
 
    result = await db["leaves"].insert_one(leave_data)
    new_leave = await db["leaves"].find_one({"_id": result.inserted_id})
 
    return convert_mongo_document(new_leave) if new_leave else None
 
async def get_leave(leave_id: str):
    db = get_db()
    leave = await db["leaves"].find_one({"_id": ObjectId(leave_id)})
    return convert_mongo_document(leave) if leave else None
 
async def get_all_leaves():
    db = get_db()
    leaves = await db["leaves"].find().to_list(100)
    return convert_many(leaves)
 
async def update_leave(leave_id: str, update_data: dict):
    db = get_db()
    update_data = normalize_document(update_data)
 
    await db["leaves"].update_one({"_id": ObjectId(leave_id)}, {"$set": update_data})
    updated = await db["leaves"].find_one({"_id": ObjectId(leave_id)})
 
    return convert_mongo_document(updated) if updated else None

#Updae leave and deduct from annual paid leaves if approved
async def update_leave_and_deduct(leave_id: str, update_data: dict):        
    db = get_db()
    update_data = normalize_document(update_data)
 
    #Fetch existing leave
    existing_leave = await db["leaves"].find_one({"_id": ObjectId(leave_id)})
    if not existing_leave:
        return None

    #If status is being updated to Approved, deduct from employee's annual paid leaves
    if update_data.get("status") == LeaveStatus.APPROVED and existing_leave.get("status") != LeaveStatus.APPROVED:
        employee_id = existing_leave["employee_id"]
        start_date = existing_leave["start_date"]
        end_date = existing_leave["end_date"]
        
        #Calculate number of days for the leave
        leave_days = (end_date - start_date).days + 1
        
        #Fetch employee details
        employee = await db["employees"].find_one({"_id": ObjectId(employee_id)})
        if not employee:
            return None
        
        leaves_remaining = employee.get("annual_paid_leaves", 0)
        
        #Deduct leaves
        if leaves_remaining >= leave_days:
            await db["employees"].update_one(
                {"_id": ObjectId(employee_id)},
                {"$inc": {"annual_paid_leaves": -leave_days}}
            )
        else:
            #Not enough balance, set to zero
            await db["employees"].update_one(
                {"_id": ObjectId(employee_id)},
                {"$set": {"annual_paid_leaves": 0}}
            )
    
    #Update the leave record
    await db["leaves"].update_one({"_id": ObjectId(leave_id)}, {"$set": update_data})
    updated = await db["leaves"].find_one({"_id": ObjectId(leave_id)})
 
    return convert_mongo_document(updated) if updated else None
 
async def delete_leave(leave_id: str):
    db = get_db()
    result = await db["leaves"].delete_one({"_id": ObjectId(leave_id)})
    return {"deleted": result.deleted_count > 0}