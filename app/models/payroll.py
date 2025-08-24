from pydantic import BaseModel, Field
from datetime import datetime
from app.models.common import DBModelMixin, PyObjectId

class PayrollBase(BaseModel):
    employee_id: PyObjectId
    month: str  # e.g. "Aug-2025"

class PayrollInDB(DBModelMixin, PayrollBase):
    base_salary: float
    deductions: float
    net_salary: float
    generated_on: datetime = Field(default_factory=datetime.utcnow)
    detail: dict | None = None  # to store breakdown like unpaid_days, per_day_rate, etc.