from pydantic import BaseModel

class ScoreSchema(BaseModel):
    marks: int
    student_id: int
    test_id: int

class ScoreResponse(BaseModel):
    id: int
    marks: int
    status: str
    test_id: int
    student_id: int

    class Config:
        from_attributes = True