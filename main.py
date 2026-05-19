from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.v1 import api
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "ALGORITHM",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "REFRESH_TOKEN_EXPIRE_DAYS"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Missing required environment variable: {var}")
    logger.info("All environment variables loaded successfully")
    yield

app = FastAPI(lifespan=lifespan)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
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


app.include_router(api)
