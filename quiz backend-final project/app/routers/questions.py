"""
routers/questions.py
--------------------
FastAPI router for all Question-related API endpoints.

Endpoints:
    POST   /questions          - Create a new question
    GET    /questions          - Retrieve all questions (with optional category filter)
    GET    /questions/{id}     - Retrieve a specific question by ID
    PUT    /questions/{id}     - Update an existing question
    DELETE /questions/{id}     - Delete a question (and its choices, via cascade)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "/",
    response_model=schemas.QuestionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new quiz question",
    description="Creates a new quiz question. Optionally specify a category.",
)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
):
    """
    **Create Question** — POST /questions

    - **question_text**: The quiz question (required, non-empty string)
    - **category**: Optional category/domain (e.g., 'Programming', 'Mathematics')
    """
    return crud.create_question(db=db, question=question)


@router.get(
    "/",
    response_model=List[schemas.QuestionOut],
    summary="Get all quiz questions",
    description="Retrieves all quiz questions. Use `category` query param to filter by domain.",
)
def get_all_questions(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=500, description="Max records to return"),
    category: Optional[str] = Query(default=None, description="Filter by category name"),
    db: Session = Depends(get_db),
):
    """
    **Get All Questions** — GET /questions

    Supports pagination via `skip` & `limit`, and optional `category` filtering.
    Each question in the response includes its associated answer choices.
    """
    return crud.get_questions(db=db, skip=skip, limit=limit, category=category)


@router.get(
    "/{question_id}",
    response_model=schemas.QuestionOut,
    summary="Get a question by ID",
    description="Retrieves a single quiz question by its unique ID, including its choices.",
)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    **Get Question by ID** — GET /questions/{id}

    Returns the question with all its choices, or 404 if not found.
    """
    db_question = crud.get_question(db=db, question_id=question_id)
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id={question_id} not found.",
        )
    return db_question


@router.put(
    "/{question_id}",
    response_model=schemas.QuestionOut,
    summary="Update a question",
    description="Updates an existing question's text and/or category. Supports partial updates.",
)
def update_question(
    question_id: int,
    question_data: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
):
    """
    **Update Question** — PUT /questions/{id}

    All fields are optional — only provided fields will be updated (PATCH-style behaviour).
    """
    updated = crud.update_question(db=db, question_id=question_id, question_data=question_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id={question_id} not found.",
        )
    return updated


@router.delete(
    "/{question_id}",
    response_model=schemas.QuestionOut,
    summary="Delete a question",
    description="Deletes a question and ALL its associated answer choices (cascade delete).",
)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """
    **Delete Question** — DELETE /questions/{id}

    This also deletes all choices linked to the question via cascade.
    Returns the deleted question data, or 404 if not found.
    """
    deleted = crud.delete_question(db=db, question_id=question_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id={question_id} not found.",
        )
    return deleted
