from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from dependencies import get_db
import models
from schemas.student import StudentSchema,StudentResponse
from schemas.auth import LoginSchema, TokenResponse
from utils import hash_password,verify_password,create_access_token
from limiter import limiter
from fastapi import Request

router = APIRouter()

@router.post("/register", response_model=StudentResponse)
@limiter.limit("5/minute")
def register(request: Request, student: StudentSchema, db: Session = Depends(get_db)):
    existing_email = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_roll = db.query(models.Student).filter(models.Student.roll_no == student.roll_no).first()
    if existing_roll:
        raise HTTPException(status_code=400, detail="Roll number already registered")

    year = (student.semester + 1) // 2

    hashed = hash_password(student.password)
    db_user = models.Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        roll_no=student.roll_no,
        semester=student.semester,
        year=year,
        faculty=student.faculty,
        dob=student.dob,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginSchema, db: Session = Depends(get_db)):
    # Check Student
    user = db.query(models.Student).filter(models.Student.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    # Check Teacher
    user = db.query(models.Teacher).filter(models.Teacher.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    # Check Admin
    user = db.query(models.Admin).filter(models.Admin.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")