from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

class TestSchema(BaseModel):
    name: str
    full_mark: int
    pass_mark: int
    date: datetime
    subject_id: int

    @field_validator('name')
    def name_must_be_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Test name must be at least 3 characters')
        return v.strip()

    @field_validator('full_mark')
    def full_mark_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError('Full mark must be greater than 0')
        return v

    @field_validator('pass_mark')
    def pass_mark_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError('Pass mark must be greater than 0')
        return v

    @field_validator('date')
    def date_must_be_future(cls, v):
        if v < datetime.utcnow():
            raise ValueError('Test date must be in the future')
        return v

    @model_validator(mode='after')
    def pass_mark_cannot_exceed_full_mark(self):
        if self.pass_mark > self.full_mark:
            raise ValueError('Pass mark cannot exceed full mark')
        return self

class TestResponse(BaseModel):
    id: int
    name: str
    full_mark: int
    pass_mark: int
    date: datetime
    subject_id: int

    class Config:
        from_attributes = True