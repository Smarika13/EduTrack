from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.student import StudentSchema, StudentResponse
from schemas.auth import LoginSchema, TokenResponse, RefreshTokenRequest
from limiter import limiter
from fastapi import Request
import services.auth_service as auth_service

router = APIRouter()


@router.post("/register", response_model=StudentResponse)
@limiter.limit("5/minute")
def register(request: Request, student: StudentSchema, db: Session = Depends(get_db)):
    return auth_service.register(student, db)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginSchema, db: Session = Depends(get_db)):
    return auth_service.login(credentials, db)


@router.post("/refresh")
def refresh_token(request_body: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_token(request_body, db)
