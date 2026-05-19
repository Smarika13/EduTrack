from pydantic import BaseModel, field_validator
from datetime import datetime


class AssignmentSchema(BaseModel):
    title: str
    description: str
    deadline: datetime
    subject_id: int

    @field_validator('title')
    def title_must_be_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        return v.strip()

    @field_validator('description')
    def description_must_be_valid(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Description cannot be empty')
        return v.strip()

    @field_validator('deadline')
    def deadline_must_be_future(cls, v):
        if v < datetime.utcnow():
            raise ValueError('Deadline must be in the future')
        return v


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    subject_id: int
    teacher_id: int

    class Config:
        from_attributes = True
