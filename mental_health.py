# mental_health.py

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date


class MentalHealth(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    relationship_status: str = Field(..., min_length=1, max_length=50)
    bothered_by_worries: int = Field(..., ge=1, le=5)
    difficulty_concentrating: int = Field(..., ge=1, le=5)
    comparison_feelings: int = Field(..., ge=1, le=5)
    feel_depressed: int = Field(..., ge=1, le=5)
    fluctuation_interest: int = Field(..., ge=1, le=5)
    sleep_issues: int = Field(..., ge=1, le=5)
    date: str


# Modelos auxiliares para entradas y actualizaciones

class MentalHealthCreate(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    relationship_status: str = Field(..., min_length=1, max_length=50)
    bothered_by_worries: int = Field(..., ge=1, le=5)
    difficulty_concentrating: int = Field(..., ge=1, le=5)
    comparison_feelings: int = Field(..., ge=1, le=5)
    feel_depressed: int = Field(..., ge=1, le=5)
    fluctuation_interest: int = Field(..., ge=1, le=5)
    sleep_issues: int = Field(..., ge=1, le=5)
    date: str


class MentalHealthUpdate(SQLModel):
    age: Optional[int] = Field(None, ge=10, le=100)
    gender: Optional[str] = Field(None, min_length=1, max_length=30)
    relationship_status: Optional[str] = Field(None, min_length=1, max_length=50)
    bothered_by_worries: Optional[int] = Field(None, ge=1, le=5)
    difficulty_concentrating: Optional[int] = Field(None, ge=1, le=5)
    comparison_feelings: Optional[int] = Field(None, ge=1, le=5)
    feel_depressed: Optional[int] = Field(None, ge=1, le=5)
    fluctuation_interest: Optional[int] = Field(None, ge=1, le=5)
    sleep_issues: Optional[int] = Field(None, ge=1, le=5)
    date: Optional[str] = None


class MentalHealthResponse(SQLModel):
    id: int
    age: int
    gender: str
    relationship_status: str
    bothered_by_worries: int
    difficulty_concentrating: int
    comparison_feelings: int
    feel_depressed: int
    fluctuation_interest: int
    sleep_issues: int
    date: str
