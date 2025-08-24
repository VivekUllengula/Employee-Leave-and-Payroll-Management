# app/services/leave_service.py
 
from datetime import date

from fastapi import HTTPException

from bson import ObjectId
 
 
async def request_leave(db, employee_id: str, start_date: date, end_date: date, reason: str) -> dict:

    """

    Create a leave request (status=Pending).

    """

    leave_doc = {

        "employee_id": ObjectId(employee_id),

        "start_date": start_date,

        "end_date": end_date,

        "status": "Pending",

        "reason": reason,

    }

    res = await db.leaves.insert_one(leave_doc)

    return await db.leaves.find_one({"_id": res.inserted_id})
 
 
async def update_leave_status(db, leave_id: str, status: str) -> dict:

    """

    Approve or Reject a leave request.

    """

    if status not in ["Approved", "Rejected"]:

        raise HTTPException(status_code=400, detail="Status must be Approved or Rejected")
 
    leave = await db.leaves.find_one({"_id": ObjectId(leave_id)})

    if not leave:

        raise HTTPException(status_code=404, detail="Leave not found")
 
    await db.leaves.update_one({"_id": leave["_id"]}, {"$set": {"status": status}})

    return await db.leaves.find_one({"_id": leave["_id"]})
 
 
async def get_approved_leaves_in_month(db, employee_id, year: int, month: int):

    """

    Get all approved leaves overlapping a given month.

    """

    from calendar import monthrange

    month_start = date(year, month, 1)

    month_end = date(year, month, monthrange(year, month)[1])
 
    cursor = db.leaves.find({

        "employee_id": employee_id,

        "status": "Approved",

        "start_date": {"$lte": month_end},

        "end_date": {"$gte": month_start}

    })
 
    return [doc async for doc in cursor]

 