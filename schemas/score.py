from pydantic import BaseModel, field_validator


class ScoreSchema(BaseModel):
    marks: int
    student_id: int
    test_id: int

    @field_validator('marks')
    def marks_must_be_valid(cls, v):
        if v < 0:
            raise ValueError('Marks cannot be negative')
        return v


class ScoreResponse(BaseModel):
    id: int
    marks: int
    status: str
    test_id: int
    student_id: int

    class Config:
        from_attributes = True
