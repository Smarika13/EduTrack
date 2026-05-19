from pydantic import field_validator, BaseModel
from datetime import date
from schemas.base import BaseUserSchema


class StudentSchema(BaseUserSchema):
    roll_no: str
    semester: int
    dob: date

    @field_validator('semester')
    def semester_must_be_valid(cls, v):
        if v < 1 or v > 8:
            raise ValueError('Semester must be between 1 and 8')
        return v

    @field_validator('roll_no')
    def roll_no_must_be_valid(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Roll number cannot be empty')
        return v.strip()


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    roll_no: str
    semester: int
    faculty: str
    year: int
    dob: date

    class Config:
        from_attributes = True
