from pydantic import field_validator, BaseModel
from schemas.base import BaseUserSchema


class TeacherSchema(BaseUserSchema):
    department: str
    qualification: str

    @field_validator('qualification')
    def qualification_must_be_valid(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Qualification cannot be empty')
        return v.strip()

    @field_validator('department')
    def department_must_be_valid(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Department cannot be empty')
        return v.strip()


class TeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    department: str
    faculty: str
    qualification: str

    class Config:
        from_attributes = True
