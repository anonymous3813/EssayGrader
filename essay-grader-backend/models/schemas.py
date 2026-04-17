import pydantic
from typing import List, Literal
from pydantic import BaseModel, computed_field, Field

ScoringType = Literal["points", "band", "hybrid"]
RubricType = Literal["APUSH", "IELTS"]


class RubricCriteria(pydantic.BaseModel):
    name: str
    description: str
    weight: float = 1
    possible_points: int


class Rubric(pydantic.BaseModel):
    rubric_type: str
    scoring_type: ScoringType
    criteria_list: list[RubricCriteria]


class Input(pydantic.BaseModel):
    question: str
    essay: str
    rubric: Rubric


# Model Output per Criterion

class CriteriaOutput(pydantic.BaseModel):
    criteria_name: str

    actual_score: float = 0.0

    possible_score: float | None = None
    band_score: float | None = None

    weaknesses: list[str] = Field(
        description="Specific weaknesses, quote or paraphrase the essay"
    )
    strengths: list[str] = Field(
        description="Specific strengths, quote or paraphrase the essay"
    )
    reasoning: str = Field(
        description=(
            "Justify score using strengths/weaknesses. "
            "Explain what is needed to improve."
        )
    )

# Final Grading Report

class EssayGradingReport(BaseModel):
    scoring_type: ScoringType
    criteria_breakdown: List[CriteriaOutput]

    strengths: List[str]
    areas_for_improvement: List[str]
    final_feedback: str

    @computed_field
    @property
    def total_possible_score(self) -> float:
        return sum(
            c.possible_score or 0 for c in self.criteria_breakdown
        )

    @computed_field
    @property
    def overall_score(self) -> float:
        scores = self.criteria_breakdown

        if not scores:
            return 0.0

        # IELTS / band-based scoring
        if self.scoring_type == "band":
            avg = sum(c.band_score or 0 for c in scores) / len(scores)
            return round(avg * 2) / 2  # nearest 0.5

        # points-based scoring
        return sum(c.actual_score for c in scores)
