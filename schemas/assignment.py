from pydantic import BaseModel
from datetime import datetime

class AssignmentSchema(BaseModel):
    title: str
    description: str
    deadline: datetime
    subject_id: int

class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    subject_id: int
    teacher_id: int

    class Config:
        from_attributes = True