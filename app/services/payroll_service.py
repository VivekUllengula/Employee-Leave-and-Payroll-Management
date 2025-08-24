from datetime import datetime, date
from calendar import monthrange
from fastapi import HTTPException
 
from app.services.leave_service import get_approved_leaves_in_month
 
 
async def generate_monthly_payroll(db, employee: dict, month_label: str) -> dict:
    """
    Generate or update monthly payroll for an employee.
    Args:
        db: Motor async database instance
        employee: MongoDB employee document
        month_label: String like "Aug-2025"
    Returns:
        Payroll document (dict)
    """
 
    # --- Step 1: Parse the month label ---
    try:
        month_dt = datetime.strptime(month_label, "%b-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid month format. Use Mon-YYYY (e.g. Aug-2025).")
 
    year, month = month_dt.year, month_dt.month
    days_in_month = monthrange(year, month)[1]
 
    # --- Step 2: Get approved leaves overlapping this month ---
    leaves = await get_approved_leaves_in_month(db, employee["_id"], year, month)
 
    def overlap_days(start: date, end: date, year: int, month: int) -> int:
        """
        Calculate overlapping leave days within the given month.
        """
        month_start = date(year, month, 1)
        month_end = date(year, month, days_in_month)
        real_start = max(start, month_start)
        real_end = min(end, month_end)
        return max(0, (real_end - real_start).days + 1)
 
    total_leave_days = sum(overlap_days(lv["start_date"], lv["end_date"], year, month) for lv in leaves)
 
    # --- Step 3: Split into paid vs unpaid days ---
    remaining_paid = employee.get("annual_paid_leaves", 0)
    paid_days = min(remaining_paid, total_leave_days)
    unpaid_days = max(0, total_leave_days - paid_days)
 
    # --- Step 4: Update employee's remaining paid leaves ---
    if paid_days > 0:
        await db.employees.update_one({"_id": employee["_id"]}, {"$inc": {"annual_paid_leaves": -paid_days}})
 
    # --- Step 5: Salary calculations ---
    base_salary = employee["salary"]
    per_day_rate = base_salary / days_in_month
    deductions = round(unpaid_days * per_day_rate, 2)
    net_salary = round(base_salary - deductions, 2)
 
    # --- Step 6: Upsert payroll record (idempotent for the month) ---
    existing = await db.payrolls.find_one({"employee_id": employee["_id"], "month": month_label})
    detail = {
        "days_in_month": days_in_month,
        "total_leave_days": total_leave_days,
        "paid_days": paid_days,
        "unpaid_days": unpaid_days,
        "per_day_rate": round(per_day_rate, 2)
    }
 
    payroll_doc = {
        "employee_id": employee["_id"],
        "month": month_label,
        "base_salary": base_salary,
        "deductions": deductions,
        "net_salary": net_salary,
        "detail": detail,
        "generated_on": datetime.utcnow(),
    }
 
    if existing:
        await db.payrolls.update_one({"_id": existing["_id"]}, {"$set": payroll_doc})
        payroll_id = existing["_id"]
    else:
        res = await db.payrolls.insert_one(payroll_doc)
        payroll_id = res.inserted_id
 
    return await db.payrolls.find_one({"_id": payroll_id})
 
 
async def get_payroll_history(db, employee_id, limit: int = 12) -> list[dict]:
    """
    Fetch payroll history for an employee (latest first).
    """
    cursor = db.payrolls.find({"employee_id": employee_id}).sort("generated_on", -1).limit(limit)
    return [doc async for doc in cursor]