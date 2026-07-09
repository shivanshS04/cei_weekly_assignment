"""
main.py
-------
FastAPI application entry point.

Startup behaviour:
    - Automatically creates database tables on first run.
    - Registers question and choice routers.

Run the server with:
    uvicorn app.main:app --reload

API docs:
    Swagger UI : http://127.0.0.1:8000/docs
    ReDoc      : http://127.0.0.1:8000/redoc
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import choices, questions


# ──────────────────────────────────────────────
# Lifespan: auto-create DB tables at startup
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on application startup."""
    Base.metadata.create_all(bind=engine)
    yield


# ──────────────────────────────────────────────
# FastAPI application instance
# ──────────────────────────────────────────────

app = FastAPI(
    lifespan=lifespan,
    title="Quiz Backend Management API",
    description="""
## Quiz Backend Management API 🎯

A RESTful backend for creating and managing quiz questions and answer choices.

### Features
- ✅ Full **CRUD** operations for Questions and Choices
- ✅ **SQLAlchemy ORM** with SQLite database
- ✅ **Pydantic v2** request validation and response serialization
- ✅ **One-to-Many** relationship: Question → Choices (cascade delete)
- ✅ Filter questions by **category**
- ✅ Filter choices by **question_id**

### Categories Supported
`General Knowledge` · `Programming` · `Mathematics` · `Data Science` · `Business Studies` · `Aptitude`

### Getting Started
1. Run `python seed_data.py` to populate the database with 50+ sample questions.
2. Visit `/docs` for interactive API testing.
    """,
    version="1.0.0",
    contact={
        "name": "Quiz API",
        "url": "http://127.0.0.1:8000/docs",
    },
    license_info={
        "name": "MIT",
    },
)


# ──────────────────────────────────────────────
# Register routers
# ──────────────────────────────────────────────

app.include_router(questions.router)
app.include_router(choices.router)


# ──────────────────────────────────────────────
# Root endpoint
# ──────────────────────────────────────────────

@app.get("/", tags=["Root"], summary="API health check & overview")
def root():
    """
    Root endpoint — confirms the API is running and provides navigation links.
    """
    return {
        "message": "Welcome to the Quiz Backend Management API 🎯",
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc",
        "endpoints": {
            "questions": {
                "create":  "POST   /questions",
                "list":    "GET    /questions",
                "get":     "GET    /questions/{id}",
                "update":  "PUT    /questions/{id}",
                "delete":  "DELETE /questions/{id}",
            },
            "choices": {
                "create": "POST   /choices",
                "list":   "GET    /choices",
                "get":    "GET    /choices/{id}",
                "update": "PUT    /choices/{id}",
                "delete": "DELETE /choices/{id}",
            },
        },
    }
