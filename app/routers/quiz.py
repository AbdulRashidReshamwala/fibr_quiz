from fastapi import APIRouter, Depends, HTTPException

from ..services.quiz import QuizService
from ..models.quiz import CreateQuizInput
from ..dependencies import get_current_user, get_quiz_service

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.post("/create")
def ceate_quiz(
    create_quiz_input: CreateQuizInput,
    current_user=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    created_quiz = quiz_service.create_quiz(create_quiz_input, current_user)
    return created_quiz


@router.post("/get/{quiz_id}")
def get_quiz(
    quiz_id: str,
    _=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    quiz = quiz_service.get_quiz(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="quiz does not exist")
    return quiz
