from typing import List, Dict, Optional
from pydantic import BaseModel


class Option(BaseModel):
    id: str
    text: str
    score: float  # maturity level 0..5
    weight: float = 1.0


class Question(BaseModel):
    id: str
    text: str
    dimension_id: str
    options: List[Option]


class Dimension(BaseModel):
    id: str
    name: str
    pillar: str  # Process | Technology | Organization
    weight: float = 1.0


class Answer(BaseModel):
    question_id: str
    score: float  # 0..5


class SubmitAnswer(BaseModel):
    session_id: str
    question_id: str
    score: float


class StartResponse(BaseModel):
    session_id: str
    total_questions: int


class DimensionScore(BaseModel):
    dimension_id: str
    dimension_name: str
    pillar: str
    score: float


class PillarScore(BaseModel):
    pillar: str
    score: float


class AssessmentResult(BaseModel):
    session_id: str
    overall_score: float
    pillars: List[PillarScore]
    dimensions: List[DimensionScore]
    recommendations: List[str]

