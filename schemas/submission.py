from pydantic import BaseModel
from datetime import datetime


class SubmissionResponse(BaseModel):
    id: int
    status: str
    file_path: str
    submitted_at: datetime
    assignment_id: int

    class Config:
        from_attributes = True