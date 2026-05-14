from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from routers import student,teacher,assignment,submission,test,score,subject,attendance,auth
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc:HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content={
            "status":"error",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
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


