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
 
 
async def delete_leave(leave_id: str):
    db = get_db()
    result = await db["leaves"].delete_one({"_id": ObjectId(leave_id)})
    return {"deleted": result.deleted_count > 0}