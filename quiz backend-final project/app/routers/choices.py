"""
routers/choices.py
------------------
FastAPI router for all Choice-related API endpoints.

Endpoints:
    POST   /choices          - Create a new answer choice
    GET    /choices          - Retrieve all choices (optional question_id filter)
    GET    /choices/{id}     - Retrieve a specific choice by ID
    PUT    /choices/{id}     - Update an existing choice
    DELETE /choices/{id}     - Delete an answer choice
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/choices",
    tags=["Choices"],
)


@router.post(
    "/",
    response_model=schemas.ChoiceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new answer choice",
    description="Adds a new answer choice linked to an existing question.",
)
def create_choice(
    choice: schemas.ChoiceCreate,
    db: Session = Depends(get_db),
):
    """
    **Create Choice** — POST /choices

    - **choice_text**: The answer text (required, non-empty string)
    - **is_correct**: True if this is the correct answer (default: false)
    - **question_id**: ID of the question this choice belongs to (required)
    """
    # Validate that the referenced question exists
    question = crud.get_question(db=db, question_id=choice.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id={choice.question_id} not found. Cannot create choice.",
        )
    return crud.create_choice(db=db, choice=choice)


@router.get(
    "/",
    response_model=List[schemas.ChoiceOut],
    summary="Get all answer choices",
    description="Retrieves all answer choices. Filter by question_id to get choices for a specific question.",
)
def get_all_choices(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=500, description="Max records to return"),
    question_id: Optional[int] = Query(default=None, description="Filter by question ID"),
    db: Session = Depends(get_db),
):
    """
    **Get All Choices** — GET /choices

    Supports pagination via `skip` & `limit`, and optional filtering by `question_id`.
    """
    return crud.get_choices(db=db, skip=skip, limit=limit, question_id=question_id)


@router.get(
    "/{choice_id}",
    response_model=schemas.ChoiceOut,
    summary="Get a choice by ID",
    description="Retrieves a single answer choice by its unique ID.",
)
def get_choice(choice_id: int, db: Session = Depends(get_db)):
    """
    **Get Choice by ID** — GET /choices/{id}

    Returns the choice, or 404 if not found.
    """
    db_choice = crud.get_choice(db=db, choice_id=choice_id)
    if not db_choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Choice with id={choice_id} not found.",
        )
    return db_choice


@router.put(
    "/{choice_id}",
    response_model=schemas.ChoiceOut,
    summary="Update an answer choice",
    description="Updates an existing answer choice. Supports partial updates.",
)
def update_choice(
    choice_id: int,
    choice_data: schemas.ChoiceUpdate,
    db: Session = Depends(get_db),
):
    """
    **Update Choice** — PUT /choices/{id}

    All fields are optional — only provided fields will be updated.
    If question_id is changed, validates that the new question exists.
    """
    # If question_id is being updated, validate the new question exists
    if choice_data.question_id is not None:
        question = crud.get_question(db=db, question_id=choice_data.question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id={choice_data.question_id} not found.",
            )

    updated = crud.update_choice(db=db, choice_id=choice_id, choice_data=choice_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Choice with id={choice_id} not found.",
        )
    return updated


@router.delete(
    "/{choice_id}",
    response_model=schemas.ChoiceOut,
    summary="Delete an answer choice",
    description="Deletes a single answer choice by its ID.",
)
def delete_choice(choice_id: int, db: Session = Depends(get_db)):
    """
    **Delete Choice** — DELETE /choices/{id}

    Returns the deleted choice data, or 404 if not found.
    """
    deleted = crud.delete_choice(db=db, choice_id=choice_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Choice with id={choice_id} not found.",
        )
    return deleted
