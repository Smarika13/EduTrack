from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.student import StudentResponse
import models

router = APIRouter()

@router.get("/student/me", response_model=StudentResponse)
def get_my_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user