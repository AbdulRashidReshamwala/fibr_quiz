from fastapi import APIRouter, Depends, HTTPException

from ..services.quiz import QuizService
from ..models.quiz import (
    CreateQuizInput,
    AnswerQuizInput,
    GetQuizOutput,
    CreateQuizOutput,
)
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
) -> CreateQuizOutput:
    created_quiz = quiz_service.create_quiz(create_quiz_input, current_user)
    return CreateQuizOutput.parse_obj(created_quiz)


@router.get("/get/{quiz_id}")
def get_quiz(
    quiz_id: str,
    _=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
) -> GetQuizOutput:
    quiz = quiz_service.get_quiz_or_error(quiz_id)
    return GetQuizOutput.parse_obj(quiz)


@router.post("/answer/{quiz_id}")
def answer_quiz(
    quiz_id: str,
    answers_submitted: AnswerQuizInput,
    current_user=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    quiz_service.submit_answer(quiz_id, answers_submitted, current_user)
    return {"msg": "submitted sucessfully"}


@router.get("/results/{quiz_id}")
def get_results(
    quiz_id: str,
    current_user=Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    if current_user["uid"] != quiz_service.get_quiz_or_error(quiz_id=quiz_id)["owner"]:
        raise HTTPException(status_code=401, detail="not authorized")
    results = quiz_service.get_results(quiz_id)
    return results
