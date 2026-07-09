"""
models.py
---------
SQLAlchemy ORM models for the Quiz application.

Relationships:
    Question (1) ──── (*) Choice
    - A Question can have many Choices.
    - A Choice belongs to exactly one Question.
    - Deleting a Question cascades and deletes all its Choices.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Question(Base):
    """Represents a quiz question stored in the 'questions' table."""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    category = Column(String, nullable=True)

    # One-to-many: one question has many choices
    # cascade="all, delete-orphan" ensures choices are deleted with the question
    choices = relationship(
        "Choice",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class Choice(Base):
    """Represents an answer choice for a quiz question, stored in 'choices' table."""

    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    # Many-to-one: many choices belong to one question
    question = relationship("Question", back_populates="choices")
