from fastapi import APIRouter, HTTPException
from models.schemas import Input, EssayGradingReport
from services.grader import get_essay_report as evaluate_essay, construct_prompt_contents, rubric_to_markdown

router = APIRouter(prefix="/grader", tags=["grader"])


@router.post("/grade", response_model=EssayGradingReport)
def get_essay_report(request: Input) -> EssayGradingReport:
    """Grade an essay against a provided rubric."""
    try:
        ai_prompt = construct_prompt_contents(request.question, request.essay, rubric_to_markdown(request.rubric.criteria_list))
        print(ai_prompt)
        return evaluate_essay(ai_prompt, request.rubric.rubric_type)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading failed: {e}")
