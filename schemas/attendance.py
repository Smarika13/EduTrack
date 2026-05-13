from pydantic import BaseModel
from datetime import datetime

class AttendanceResponse(BaseModel):
    id: int
    date: datetime
    status: str
    subject_id: int

    class Config:
        from_attributes = True