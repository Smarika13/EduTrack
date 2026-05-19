from pydantic import BaseModel, field_validator
from datetime import datetime


class AttendanceSchema(BaseModel):
    date: datetime
    status: str
    student_id: int
    subject_id: int

    @field_validator('status')
    def status_must_be_valid(cls, v):
        allowed = ['present', 'absent']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v.lower()


class AttendanceResponse(BaseModel):
    id: int
    date: datetime
    status: str
    subject_id: int

    class Config:
        from_attributes = True
