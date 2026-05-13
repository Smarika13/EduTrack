from pydantic import BaseModel
from datetime import datetime

class TestSchema(BaseModel):
    name: str
    full_mark: int
    pass_mark: int
    date: datetime
    subject_id: int

class TestResponse(BaseModel):
    id: int
    name: str
    full_mark: int
    pass_mark: int
    date: datetime
    subject_id: int

    class Config:
        from_attributes = True