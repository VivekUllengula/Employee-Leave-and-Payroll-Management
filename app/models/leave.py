from pydantic import BaseModel, Field
from datetime import date, datetime
from app.models.common import DBModelMixin, PyObjectId

class LeaveStatus:
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class LeaveBase(BaseModel):
    employee_id: PyObjectId
    start_date: date
    end_date: date
    reason: str | None = None

class LeaveCreate(LeaveBase):
    pass

class LeaveInDB(DBModelMixin, LeaveBase):
    status: str = Field(default=LeaveStatus.PENDING)
    requested_on: datetime = Field(default_factory=datetime.utcnow)
    approved_rejected_on: datetime | None = None

class LeaveAction(BaseModel):
    note: str | None = None