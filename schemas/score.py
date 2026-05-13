from pydantic import BaseModel

class ScoreResponse(BaseModel):
    id: int
    marks: int
    status: str
    test_id: int

    class Config:
        from_attributes = True