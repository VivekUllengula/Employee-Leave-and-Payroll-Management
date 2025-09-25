import calendar
from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db
from app.utils.mongo_helpers import convert_mongo_document, convert_many, normalize_document
 
# Generate Payroll for an Employee
async def generate_payroll(employee_id: str, month: int, year: int):
    db = get_db()

    #Fetch employee and details
    employee = await db["employees"].find_one({"_id": ObjectId(employee_id)})
    if not employee:
        return None
    
    base_salary = employee.get("salary", 0)
    leaves_remaining = employee.get("annual_paid_leaves", 0)

    #Get the days in a month and per day salary for that month
    total_days = calendar.monthrange(year, month)[1]
    per_day_salary = base_salary / total_days

    #Get all the approved leaves in the month
    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, total_days)

    approved_leaves = await db["leaves"].find({
        "employee_id": str(employee["_id"]),
        "status": "Approved",
        "start_date": {"$lte": end_of_month},
        "end_date": {"$gte": start_of_month}
    }).to_list(None)

    leave_days = 0
    for leave in approved_leaves:
        leave_start = max(leave["start_date"], start_of_month )
        leave_end = min(leave["end_date"], end_of_month)
        leave_days += (leave_end - leave_start).days + 1

    # Calculating the deductions

    deduction_days = 0
    if leave_days > 0:
        if leaves_remaining >= leave_days:
            #Deduct only from balance
            await db["employees"].update_one(
                {"_d": ObjectId(employee_id)},
                {"$inc": {"annual_paid_leaves": -leave_days}}
            )
    else:
        deduction_days = leave_days - leaves_remaining
        await db["employees"].update_one(
            {"_d": ObjectId(employee_id)},
                {"$set": {"annual_paid_leaves": 0}}
            )
        
    deduction_days = max(deduction_days, 0)    
    deductions = round(deduction_days * per_day_salary, 2)
    net_salary = round(base_salary - deductions, 2)

    #Save payroll record
    payroll_doc = {
        "employee_id": str(employee["_id"]),
        "month": f"{year}-{month:02d}",
        "base_salary": base_salary,
        "deductions": round(deductions, 2),
        "net_salary": round(net_salary, 2),
        "generated_at": datetime.utcnow(),
        "detail": {
            "total_days": total_days,
            "leave_days": leave_days,
            "deduction_days": deduction_days,
            "per_day_salary": round(per_day_salary, 2),
        }
    }

    result = await db["payrolls"].insert_one(payroll_doc)
    new_payroll = await db["payrolls"].find_one({"_id": result.inserted_id})
    return convert_mongo_document(new_payroll) if new_payroll else None
 
# Get Payroll by ID
async def get_payroll(payroll_id: str):
    db = get_db()
    payroll = await db["payrolls"].find_one({"_id": ObjectId(payroll_id)})
    return convert_mongo_document(payroll) if payroll else None
 
# Get All Payrolls
async def get_all_payrolls():
    db = get_db()
    payrolls = await db["payrolls"].find().to_list(100)
    return convert_many(payrolls)
 
# Update Payroll (e.g., corrections/adjustments)
async def update_payroll(payroll_id: str, update_data: dict):
    db = get_db()
    update_data = normalize_document(update_data)
    await db["payrolls"].update_one({"_id": ObjectId(payroll_id)}, {"$set": update_data})
    updated = await db["payrolls"].find_one({"_id": ObjectId(payroll_id)})
    return convert_mongo_document(updated) if updated else None
 
# Delete Payroll
async def delete_payroll(payroll_id: str):
    db = get_db()
    result = await db["payrolls"].delete_one({"_id": ObjectId(payroll_id)})
    return {"deleted": result.deleted_count > 0}