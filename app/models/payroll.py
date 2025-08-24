from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.common import DBModelMixin, PyObjectId
 
class PayrollBase(BaseModel):
    employee_id: PyObjectId = Field(..., description="Employee ID (ObjectId)")
    month: str = Field(..., description="Month label, e.g. 'Aug-2025'")
 
class PayrollCreate(PayrollBase):
    """Payload to generate/create a payroll record."""
    base_salary: float = Field(..., description="Base salary for the month")
    deductions: float = Field(0.0, description="Total deductions")
    detail: Optional[dict] = Field(None, description="Breakdown (unpaid_days, per_day_rate, etc.)")
 
class PayrollUpdate(BaseModel):
    """Partial update for a payroll record."""
    month: Optional[str] = None
    base_salary: Optional[float] = None
    deductions: Optional[float] = None
    detail: Optional[dict] = None
    generated_on: Optional[datetime] = None
    net_salary: Optional[float] = None  # allow manual override if needed
 
class PayrollInDB(DBModelMixin, PayrollBase):
    base_salary: float
    deductions: float
    net_salary: float
    generated_on: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    detail: Optional[dict] = None

 