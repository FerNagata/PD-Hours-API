from pydantic import BaseModel, Field
from datetime import datetime

class SquadBase(BaseModel):
    name: str = Field(...)

class SquadRead(SquadBase):
    id: int = Field(...)

class EmployeeHours(BaseModel):
    employee_id: int = Field(alias='employeeId')
    employee_name: str = Field(alias='employeeName')
    spent_hours: float = Field(alias='spentHours')

class TotalHours(BaseModel):
    squad_id: int = Field(alias='squadId')
    squad_name: str = Field(alias='squadName')
    total_hours: int = Field(alias='totalHours')

class AverageHours(BaseModel):
    squad_id: int = Field(alias='squadId')
    average_hours_per_day: float = Field(alias='averageHoursPerDay')