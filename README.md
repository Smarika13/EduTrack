# EduTrack — Education Management REST API

A production-structured backend REST API for managing school workflows across three roles: **Student**, **Teacher**, and **Admin**. Built with real architectural decisions — service layer separation, Redis cache-aside pattern with active invalidation, refresh token rotation, rate limiting, and a CI/CD pipeline with branch protection.

Built with **Python + FastAPI**, following real-world backend architecture patterns.

---

## Features

### Authentication & Security
- JWT-based authentication with **access token + refresh token** rotation
- **bcrypt** password hashing
- Role-based access control (Student / Teacher / Admin)
- **Rate limiting** on login and registration endpoints (5 requests/minute)

### Core Functionality

| Role    | Capabilities |
|---------|-------------|
| Student | Register, Login, View profile, View attendance, View test scores, Submit assignments |
| Teacher | Login, View profile, Mark attendance, Enter test scores, Create assignments, Create tests |
| Admin   | Create teacher accounts, Create subjects |

### Backend Architecture
- **Service layer** — business logic separated from HTTP routing; reusable across endpoints
- **Pagination** — all list endpoints return `total`, `page`, `limit`, `data`
- **Redis caching** — cache-aside pattern with active cache invalidation on writes
- **File uploads/downloads** — PDF assignment submissions stored on disk
- **Structured logging** — file + console handlers with severity levels
- **Global error handling** — consistent JSON error responses across all endpoints
- **Environment variable validation** — server refuses to start if required vars are missing
- **Alembic migrations** — database schema versioned and managed

### DevOps
- **GitHub Actions CI** — runs `flake8` linting on every push and PR
- **Branch protection** — direct pushes to `main` are blocked; PRs required with CI passing before merge
- **API versioning** — all endpoints under `/api/v1/`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (development) |
| Cache | Redis |
| Auth | JWT (python-jose), bcrypt |
| Migrations | Alembic |
| Rate Limiting | SlowAPI |
| CI | GitHub Actions + flake8 |

---

## Project Structure

```
EduTrack/
├── routers/
│   └── v1/               # HTTP layer — routes, auth checks, responses
│       ├── auth.py
│       ├── student.py
│       ├── teacher.py
│       ├── attendance.py
│       ├── assignment.py
│       ├── submission.py
│       ├── score.py
│       ├── subject.py
│       └── test.py
├── services/             # Business logic layer — DB ops, cache, validations
│   ├── auth_service.py
│   ├── student_service.py
│   ├── teacher_service.py
│   ├── attendance_service.py
│   ├── assignment_service.py
│   ├── submission_service.py
│   ├── score_service.py
│   ├── subject_service.py
│   └── test_service.py
├── schemas/              # Pydantic request/response models
├── models.py             # SQLAlchemy database models
├── database.py           # Engine, session, base
├── dependencies.py       # get_db dependency
├── utils.py              # JWT, password hashing, pagination helper
├── caching.py            # Redis connection
├── logger.py             # Logging configuration
├── limiter.py            # Rate limiter setup
├── main.py               # App entry point, middleware, exception handlers
├── .github/
│   └── workflows/
│       └── ci.yaml       # GitHub Actions CI pipeline
└── alembic/              # Database migration files
```

---

## API Endpoints

### Auth
```
POST   /api/v1/register          — Student registration
POST   /api/v1/login             — Login (returns access + refresh token)
POST   /api/v1/refresh           — Get new access token
```

### Student
```
GET    /api/v1/student/me                — Get own profile
GET    /api/v1/student/me/attendance     — Get own attendance (paginated, cached)
GET    /api/v1/student/me/scores         — Get own test scores (paginated)
GET    /api/v1/student/me/submissions    — Get own submissions (paginated)
```

### Teacher
```
GET    /api/v1/teacher/me                — Get own profile
POST   /api/v1/attendance                — Mark student attendance
POST   /api/v1/score                     — Enter test score
POST   /api/v1/assignment                — Create assignment
POST   /api/v1/test                      — Create test
```

### Submission
```
POST   /api/v1/submission                            — Submit assignment (PDF)
PUT    /api/v1/submission/assignment/{id}             — Update submission
DELETE /api/v1/submission/assignment/{id}             — Delete submission
GET    /api/v1/submission/assignment/{id}/download    — Download submission
```

### Admin
```
POST   /api/v1/subject                  — Create subject
POST   /api/v1/admin/teacher            — Create teacher account
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- Redis server running locally

### Installation

```bash
# Clone the repository
git clone https://github.com/Smarika13/EduTrack.git
cd EduTrack

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./edutrack.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://localhost:6379
```

### Run Migrations

```bash
alembic upgrade head
```

### Start the Server

```bash
uvicorn main:app --reload
```

API will be available at: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

---

## Architecture Decisions

**Why service layer?**
Routers handle only HTTP concerns (auth checks, request/response). All business logic, DB operations, and cache management live in the service layer. This means business rules can be reused across multiple endpoints without duplication.

**Why Redis caching?**
Student attendance is read far more often than it is written. Cache-aside pattern stores responses in Redis with a 24-hour TTL. Cache is actively deleted (not updated) on write operations because the exact pagination parameters of the cached response are unknown — updating would require knowing which cached pages exist.

**Why refresh tokens?**
Access tokens are stateless — they cannot be invalidated before expiry. Keeping them short-lived (30 min) limits the damage window if stolen. Refresh tokens are stored in the database and can be immediately revoked on logout.

---

## CI/CD

Every push and pull request triggers the CI pipeline:

```yaml
- Checkout code
- Set up Python 3.11
- Install dependencies
- Run flake8 linting
```

**Branch protection is enforced** — direct pushes to `main` are blocked. All changes must go through a pull request, and CI must pass before merging. This ensures no broken or unformatted code reaches the main branch.

---

## Author

**Smarika** — [GitHub](https://github.com/Smarika13)