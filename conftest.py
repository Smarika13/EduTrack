import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from dependencies import get_db
from sqlalchemy.pool import StaticPool
from utils import hash_password
import models
from unittest.mock import AsyncMock
from caching import get_redis

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    from limiter import limiter

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    async def override_get_redis():
        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value=None)
        mock_redis.set = AsyncMock()
        mock_redis.delete = AsyncMock()
        yield mock_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    limiter.enabled = False
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_user(db):
    hashed = hash_password("TestAdmin@123")
    admin = models.Admin(name="Test Admin", email="admin@test.com", hashed_password=hashed)
    db.add(admin)
    db.commit()
    return {"email": "admin@test.com", "password": "TestAdmin@123"}
