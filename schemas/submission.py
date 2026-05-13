from pydantic import BaseModel
from datetime import datetime

class SubmissionSchema(BaseModel):
    assignment_id: int
    file_path: str

class SubmissionResponse(BaseModel):
    id: int
    status: str
    file_path: str
    submitted_at: datetime
    assignment_id: int

    class Config:
        from_attributes = True