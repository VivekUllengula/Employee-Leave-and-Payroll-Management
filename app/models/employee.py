from pydantic import BaseModel, Field
from datetime import date
from app.models.common import DBModelMixin

class EmployeeBase(BaseModel):
    name: str
    designation: str
    salary: float = Field(gt=0)
    contact: str
    join_date: date
    annual_paid_leaves: int = Field(default=24, ge=0)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: str | None = None
    designation: str | None = None
    salary: float | None = Field(default=None, gt=0)
    contact: str | None = None
    annual_paid_leaves: int | None = Field(default=None, ge=0)

class EmployeeInDB(DBModelMixin, EmployeeBase):
    pass