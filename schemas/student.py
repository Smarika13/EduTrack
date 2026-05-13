from pydantic import BaseModel
from datetime import date

class StudentSchema(BaseModel):
    name:str
    email:str
    phone:str
    roll_no:str
    semester:int
    faculty:str
    dob:date
    password :str

class StudentResponse(BaseModel):
    id:int
    name:str
    email:str
    phone:str
    roll_no:str
    semester:int
    faculty:str
    year:int
    dob:date

    class Config:
        from_attributes = True





    

