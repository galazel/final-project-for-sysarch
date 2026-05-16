from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=50)
    salary: Decimal = Field(..., gt=0)
    hire_date: datetime = Field(..., alias="hireDate")

    @validator("first_name", "last_name")
    def validate_names(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("Name must not contain numbers")
        return value

    class Config:
        from_attributes = True
        populate_by_name = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeePatch(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=2, max_length=50)
    salary: Optional[Decimal] = Field(None, gt=0)
    hire_date: Optional[datetime] = Field(None, alias="hireDate")

    class Config:
        from_attributes = True
        populate_by_name = True


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True