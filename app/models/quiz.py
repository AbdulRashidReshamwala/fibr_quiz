from typing import Optional
from pydantic import BaseModel, validator, NonNegativeInt, conlist


class QuizQuestions(BaseModel):
    question: str
    options: conlist(str, min_items=1)
    correct_options: conlist(NonNegativeInt, min_items=1)

    @validator("correct_options")
    @classmethod
    def check_correct_option(cls, value, values):
        for ele in value:
            if ele >= len(values.get("options", [])):
                raise ValueError(
                    "values in correct_options can not be greater than length of options"
                )
        return value


class CreateQuizInput(BaseModel):
    id: Optional[str] = None
    title: str
    questions: list[QuizQuestions]
