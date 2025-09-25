from fastapi import APIRouter, HTTPException, Depends
from app.services import leave_service
from app.models.leave import LeaveCreate, LeaveUpdate
from app.utils.auth import get_current_user, role_checker

router = APIRouter(prefix="/leaves", tags=["Leaves"], dependencies=[Depends(get_current_user)])
 
# Create Leave
@router.post("/")
async def create_leave(leave: LeaveCreate):
    new_leave = await leave_service.create_leave(leave.dict())
    if not new_leave:
        raise HTTPException(status_code=400, detail="Failed to create leave")
    return new_leave
 
# Get Leave by ID
@router.get("/{leave_id}")
async def get_leave(leave_id: str):
    leave = await leave_service.get_leave(leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave
 
# Get All Leaves
@router.get("/", dependencies=[Depends(role_checker(['admin', 'manager']))])
async def get_all_leaves():
    return await leave_service.get_all_leaves()
 
# Update Leave
@router.put("/{leave_id}", dependencies=[Depends(role_checker(['admin', 'manager']))])
async def update_leave(leave_id: str, leave: LeaveUpdate):
    updated_leave = await leave_service.update_leave(leave_id, leave.dict(exclude_unset=True))
    if not updated_leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return updated_leave
 
# Delete Leave
@router.delete("/{leave_id}", dependencies=[Depends(role_checker(['admin']))])
async def delete_leave(leave_id: str):
    result = await leave_service.delete_leave(leave_id)
    if not result["deleted"]:
        raise HTTPException(status_code=404, detail="Leave not found")
    return result