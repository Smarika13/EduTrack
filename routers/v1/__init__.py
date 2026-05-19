from fastapi import APIRouter
from routers.v1 import assignment, attendance, auth, score, student, subject, submission, teacher, test
api = APIRouter(prefix="/api/v1")

api.include_router(student.router, tags=["Student"])
api.include_router(teacher.router, tags=["Teacher"])
api.include_router(subject.router, tags=["Subject"])
api.include_router(submission.router, tags=["Submission"])
api.include_router(attendance.router, tags=["Attendance"])
api.include_router(test.router, tags=["Test"])
api.include_router(score.router, tags=["Score"])
api.include_router(assignment.router, tags=["Assignment"])
api.include_router(auth.router, tags=["Auth"])
