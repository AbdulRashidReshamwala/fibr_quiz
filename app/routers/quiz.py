from fastapi import APIRouter, Depends

from ..services.quiz import QuizService
from ..models.quiz import CreateQuizInput
from ..dependencies import get_quiz_service

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.post("/create")
def ceate_quiz(
    create_quiz_input: CreateQuizInput,
    quiz_service: QuizService = Depends(get_quiz_service),
):
    quiz_service.create_quiz(create_quiz_input)
    pass
