from fastapi import APIRouter, Depends, HTTPException

from ..services.quiz import QuizService
from ..models.quiz import CreateQuizInput, AnswerQuizInput
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
    quiz = quiz_service.get_quiz_or_error(quiz_id)
    return quiz


@router.post("/answer/{quiz_id}")
def answer_quiz(
    quiz_id: str,
    answers_submitted: AnswerQuizInput,
    current_user=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    quiz_service.submit_answer(quiz_id, answers_submitted, current_user)
    return {"msg": "submitted sucessfully"}


@router.post("/results/{quiz_id}")
def get_results(
    quiz_id: str,
    current_user=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    if current_user["uid"] != quiz_service.get_quiz_or_error(quiz_id=quiz_id)["owner"]:
        raise HTTPException(status_code=401, detail="not authorized")
    results = quiz_service.get_results(quiz_id)
    return results
