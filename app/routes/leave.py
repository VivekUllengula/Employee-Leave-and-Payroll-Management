from fastapi import APIRouter, Depends
from app.db.mongo import get_db
from app.services import leave_service
 
router = APIRouter(prefix="/leaves", tags=["Leaves"])
 
 
@router.post("/")
async def request_leave(leave: dict, db=Depends(get_db)):
    return await leave_service.request_leave(
        db,
        leave["employee_id"],
        leave["start_date"],
        leave["end_date"],
        leave.get("reason", "")
    )
 
 
@router.put("/{leave_id}/approve")
async def approve_leave(leave_id: str, db=Depends(get_db)):
    return await leave_service.update_leave_status(db, leave_id, "Approved")
 
 
@router.put("/{leave_id}/reject")
async def reject_leave(leave_id: str, db=Depends(get_db)):
    return await leave_service.update_leave_status(db, leave_id, "Rejected")