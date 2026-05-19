from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str
    credit_hr: int
    faculty: str
    semester: int
    teacher_id: int


class SubjectResponse(BaseModel):
    id: int
    name: str
    credit_hr: int
    faculty: str
    semester: int
    teacher_id: int

    class Config:
        from_attributes = True
