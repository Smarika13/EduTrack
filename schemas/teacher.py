from pydantic import BaseModel

class TeacherSchema(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    faculty: str
    qualification: str
    password: str

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