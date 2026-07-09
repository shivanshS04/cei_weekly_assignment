"""
crud.py
-------
Business logic layer: all database CRUD operations.

Separation of concerns:
    - Routers handle HTTP request/response.
    - crud.py handles database interactions.
    - This makes the code testable and maintainable.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


# ──────────────────────────────────────────────
# Question CRUD
# ──────────────────────────────────────────────

def get_questions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
) -> List[models.Question]:
    """
    Retrieve all questions with optional pagination and category filtering.

    Args:
        db: Database session.
        skip: Number of records to skip (for pagination).
        limit: Maximum number of records to return.
        category: If provided, filter questions by this category.

    Returns:
        List of Question ORM objects.
    """
    query = db.query(models.Question)
    if category:
        query = query.filter(models.Question.category == category)
    return query.offset(skip).limit(limit).all()


def get_question(db: Session, question_id: int) -> Optional[models.Question]:
    """
    Retrieve a single question by its primary key.

    Args:
        db: Database session.
        question_id: Primary key of the question.

    Returns:
        Question ORM object or None if not found.
    """
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
    """
    Create and persist a new question.

    Args:
        db: Database session.
        question: Validated QuestionCreate schema.

    Returns:
        The newly created Question ORM object.
    """
    db_question = models.Question(
        question_text=question.question_text,
        category=question.category,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(
    db: Session,
    question_id: int,
    question_data: schemas.QuestionUpdate,
) -> Optional[models.Question]:
    """
    Update an existing question's fields. Only provided (non-None) fields are updated.

    Args:
        db: Database session.
        question_id: Primary key of the question to update.
        question_data: QuestionUpdate schema with optional fields.

    Returns:
        Updated Question ORM object, or None if not found.
    """
    db_question = get_question(db, question_id)
    if not db_question:
        return None

    update_data = question_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)

    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int) -> Optional[models.Question]:
    """
    Delete a question and all its associated choices (cascade).

    Args:
        db: Database session.
        question_id: Primary key of the question to delete.

    Returns:
        The deleted Question ORM object, or None if not found.
    """
    db_question = get_question(db, question_id)
    if not db_question:
        return None

    db.delete(db_question)
    db.commit()
    return db_question


# ──────────────────────────────────────────────
# Choice CRUD
# ──────────────────────────────────────────────

def get_choices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    question_id: Optional[int] = None,
) -> List[models.Choice]:
    """
    Retrieve all choices with optional pagination and question filtering.

    Args:
        db: Database session.
        skip: Number of records to skip (for pagination).
        limit: Maximum number of records to return.
        question_id: If provided, filter choices by this question ID.

    Returns:
        List of Choice ORM objects.
    """
    query = db.query(models.Choice)
    if question_id:
        query = query.filter(models.Choice.question_id == question_id)
    return query.offset(skip).limit(limit).all()


def get_choice(db: Session, choice_id: int) -> Optional[models.Choice]:
    """
    Retrieve a single choice by its primary key.

    Args:
        db: Database session.
        choice_id: Primary key of the choice.

    Returns:
        Choice ORM object or None if not found.
    """
    return db.query(models.Choice).filter(models.Choice.id == choice_id).first()


def create_choice(db: Session, choice: schemas.ChoiceCreate) -> models.Choice:
    """
    Create and persist a new answer choice.

    Args:
        db: Database session.
        choice: Validated ChoiceCreate schema.

    Returns:
        The newly created Choice ORM object.
    """
    db_choice = models.Choice(
        choice_text=choice.choice_text,
        is_correct=choice.is_correct,
        question_id=choice.question_id,
    )
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice


def update_choice(
    db: Session,
    choice_id: int,
    choice_data: schemas.ChoiceUpdate,
) -> Optional[models.Choice]:
    """
    Update an existing choice's fields. Only provided (non-None) fields are updated.

    Args:
        db: Database session.
        choice_id: Primary key of the choice to update.
        choice_data: ChoiceUpdate schema with optional fields.

    Returns:
        Updated Choice ORM object, or None if not found.
    """
    db_choice = get_choice(db, choice_id)
    if not db_choice:
        return None

    update_data = choice_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_choice, field, value)

    db.commit()
    db.refresh(db_choice)
    return db_choice


def delete_choice(db: Session, choice_id: int) -> Optional[models.Choice]:
    """
    Delete a single answer choice.

    Args:
        db: Database session.
        choice_id: Primary key of the choice to delete.

    Returns:
        The deleted Choice ORM object, or None if not found.
    """
    db_choice = get_choice(db, choice_id)
    if not db_choice:
        return None

    db.delete(db_choice)
    db.commit()
    return db_choice
