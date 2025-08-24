from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.models.common import DBModelMixin, PyObjectId
 
class LeaveStatus:
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
 
class LeaveBase(BaseModel):
    employee_id: PyObjectId = Field(..., description="Employee ID (ObjectId)")
    start_date: date = Field(..., description="Leave start date")
    end_date: date = Field(..., description="Leave end date")
    reason: Optional[str] = Field(None, description="Reason for leave")
 
class LeaveCreate(LeaveBase):
    """Payload to create a leave request."""
    pass
 
class LeaveUpdate(BaseModel):
    """Partial update for a leave."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    status: Optional[Literal["Pending", "Approved", "Rejected"]] = None
    approved_rejected_on: Optional[datetime] = None
 
class LeaveInDB(DBModelMixin, LeaveBase):
    status: str = Field(default=LeaveStatus.PENDING, description="Current status")
    requested_on: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")
    approved_rejected_on: Optional[datetime] = Field(None, description="Approval/Rejection timestamp")
 
class LeaveAction(BaseModel):
    note: Optional[str] = Field(None, description="Optional note when approving/rejecting")

 