from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import student,teacher,assignment,submission,test,score,subject,attendance,auth


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(subject.router)
app.include_router(submission.router)
app.include_router(attendance.router)
app.include_router(test.router)
app.include_router(score.router)
app.include_router(assignment.router)
app.include_router(auth.router)


