from pydantic import BaseModel, Field
from datetime import datetime

class ReportBase(BaseModel):
    description: str = Field(...)
    employee_id: int = Field(alias="employeeId")
    spent_hours: int = Field(alias="spentHours")

class ReportRead(ReportBase):
    id: int = Field(...)
    created_at: datetime = Field(alias="createdAt")

class ReportsFromSquad(BaseModel):
    member: str = Field(alias="member")
    description: str = Field(alias="description")
    spent_hours: int = Field(alias="spentHours")
    created_at: datetime = Field(alias="createdAt")