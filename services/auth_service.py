from fastapi import HTTPException
import models
from logger import logger
from utils import hash_password, verify_password, create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from jose import jwt


def register(student, db):
    existing_email = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_email:
        logger.warning(f"Email already registered: {student.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_roll = db.query(models.Student).filter(models.Student.roll_no == student.roll_no).first()
    if existing_roll:
        logger.warning(f"Roll number already registered {student.email}")
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
    logger.info(f"You are registered {student.email}")
    return db_user


def login(credentials, db):
    # Check Student
    user = db.query(models.Student).filter(models.Student.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        refresh = create_refresh_token(data={"sub": user.email})
        db_refresh = models.RefreshToken(
            token=refresh,
            user_id=user.id,
            role="student",
            expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        db.add(db_refresh)
        db.commit()
        logger.info(f"You are logged in as {user.email}")
        return {"access_token": token, "token_type": "bearer", "refresh_token": refresh}

    # Check Teacher
    user = db.query(models.Teacher).filter(models.Teacher.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        refresh = create_refresh_token(data={"sub": user.email})
        db_refresh = models.RefreshToken(
            token=refresh,
            user_id=user.id,
            role="teacher",
            expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        db.add(db_refresh)
        db.commit()
        logger.info(f"You are logged in as {user.email}")
        return {"access_token": token, "token_type": "bearer", "refresh_token": refresh}

    # Check Admin
    user = db.query(models.Admin).filter(models.Admin.email == credentials.email).first()
    if user and verify_password(credentials.password, user.hashed_password):
        token = create_access_token(data={"sub": user.email})
        refresh = create_refresh_token(data={"sub": user.email})
        db_refresh = models.RefreshToken(
            token=refresh,
            user_id=user.id,
            role="admin",
            expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        db.add(db_refresh)
        db.commit()
        logger.info(f"You are logged in as {user.email}")
        return {"access_token": token, "token_type": "bearer", "refresh_token": refresh}

    logger.warning(f"Invalid credentials {credentials.email}")
    raise HTTPException(status_code=401, detail="Invalid credentials")


def refresh_token(request_body, db):
    refresh = db.query(models.RefreshToken).filter(models.RefreshToken.token == request_body.refresh_token).first()
    if not refresh:
        raise HTTPException(status_code=401, detail="No refresh token")
    if refresh.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")
    if datetime.utcnow() > refresh.expires_at:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    payload = jwt.decode(request_body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    new_token = create_access_token(data={"sub": email})
    refresh.is_revoked = True
    db.commit()
    return {"access_token": new_token, "token_type": "bearer"}
