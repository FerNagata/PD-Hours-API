from pydantic import BaseModel, Field

class EmployeeBase(BaseModel):
    name: str = Field(...)
    estimated_hours: int = Field(alias="estimatedHours")
    squad_id: int = Field(alias="squadId")

class EmployeeRead(EmployeeBase):
    id: int = Field(...)