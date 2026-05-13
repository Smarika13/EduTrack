from pydantic import BaseModel
from datetime import datetime

class AttendanceSchema(BaseModel):
    date: datetime
    status: str
    student_id: int
    subject_id: int

class AttendanceResponse(BaseModel):
    id: int
    date: datetime
    status: str
    subject_id: int

    class Config:
        from_attributes = True