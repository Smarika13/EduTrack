from pydantic import BaseModel

class AdminSchema(BaseModel):
    name: str
    email: str
    password: str

class AdminResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True