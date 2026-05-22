from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.test import TestSchema, TestResponse
import services.test_service as test_service

router = APIRouter()


@router.post("/test", response_model=TestResponse)
def create_test(test: TestSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create tests")
    return test_service.create_test(test, current_user, db)
