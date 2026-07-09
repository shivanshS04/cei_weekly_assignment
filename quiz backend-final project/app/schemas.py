"""
schemas.py
----------
Pydantic v2 models for request validation and response serialization.

Schema hierarchy:
    Choice:  ChoiceBase → ChoiceCreate | ChoiceUpdate | ChoiceOut
    Question: QuestionBase → QuestionCreate | QuestionUpdate | QuestionOut
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ──────────────────────────────────────────────
# Choice Schemas
# ──────────────────────────────────────────────

class ChoiceBase(BaseModel):
    """Shared fields for Choice schemas."""
    choice_text: str = Field(..., min_length=1, description="Text of the answer choice")
    is_correct: bool = Field(default=False, description="Whether this is the correct answer")
    question_id: int = Field(..., description="ID of the question this choice belongs to")


class ChoiceCreate(ChoiceBase):
    """Schema for creating a new Choice (POST /choices)."""
    pass


class ChoiceUpdate(BaseModel):
    """Schema for updating an existing Choice (PUT /choices/{id}).
    All fields are optional so partial updates are supported.
    """
    choice_text: Optional[str] = Field(None, min_length=1, description="Updated choice text")
    is_correct: Optional[bool] = Field(None, description="Updated correct-answer flag")
    question_id: Optional[int] = Field(None, description="Updated question ID")


class ChoiceOut(BaseModel):
    """Schema for returning Choice data in API responses."""
    id: int
    choice_text: str
    is_correct: bool
    question_id: int

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Question Schemas
# ──────────────────────────────────────────────

class QuestionBase(BaseModel):
    """Shared fields for Question schemas."""
    question_text: str = Field(..., min_length=1, description="The quiz question text")
    category: Optional[str] = Field(None, description="Category/domain of the question")


class QuestionCreate(QuestionBase):
    """
    Schema for creating a new Question (POST /questions).

    Example (from spec):
        class QuestionCreate(BaseModel):
            question_text: str
            category: str | None = None
    """
    pass


class QuestionUpdate(BaseModel):
    """Schema for updating an existing Question (PUT /questions/{id}).
    All fields are optional so partial updates are supported.
    """
    question_text: Optional[str] = Field(None, min_length=1, description="Updated question text")
    category: Optional[str] = Field(None, description="Updated category")


class QuestionOut(BaseModel):
    """Schema for returning Question data in API responses (includes nested choices)."""
    id: int
    question_text: str
    category: Optional[str]
    choices: List[ChoiceOut] = []

    model_config = {"from_attributes": True}
