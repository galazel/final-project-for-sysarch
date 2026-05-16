from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=50)

    @validator("first_name", "last_name")
    def validate_names(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("Name must not contain numbers")
        return value


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeePatch(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=2, max_length=50)


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True