from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db
from app.utils.mongo_helpers import convert_mongo_document, convert_many, normalize_document
 
# ✅ Generate Payroll for an Employee
async def generate_payroll(payroll_data: dict):
    db = get_db()
    payroll_data = normalize_document(payroll_data)
    payroll_data["generated_at"] = datetime.utcnow()
    result = await db["payrolls"].insert_one(payroll_data)
    new_payroll = await db["payrolls"].find_one({"_id": result.inserted_id})
    return convert_mongo_document(new_payroll) if new_payroll else None
 
# ✅ Get Payroll by ID
async def get_payroll(payroll_id: str):
    db = get_db()
    payroll = await db["payrolls"].find_one({"_id": ObjectId(payroll_id)})
    return convert_mongo_document(payroll) if payroll else None
 
# ✅ Get All Payrolls
async def get_all_payrolls():
    db = get_db()
    payrolls = await db["payrolls"].find().to_list(100)
    return convert_many(payrolls)
 
# ✅ Update Payroll (e.g., corrections/adjustments)
async def update_payroll(payroll_id: str, update_data: dict):
    db = get_db()
    update_data = normalize_document(update_data)
    await db["payrolls"].update_one({"_id": ObjectId(payroll_id)}, {"$set": update_data})
    updated = await db["payrolls"].find_one({"_id": ObjectId(payroll_id)})
    return convert_mongo_document(updated) if updated else None
 
# ✅ Delete Payroll
async def delete_payroll(payroll_id: str):
    db = get_db()
    result = await db["payrolls"].delete_one({"_id": ObjectId(payroll_id)})
    return {"deleted": result.deleted_count > 0}