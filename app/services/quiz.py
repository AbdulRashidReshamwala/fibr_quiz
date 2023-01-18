import uuid

from fastapi import HTTPException
from firebase_admin import firestore


class QuizService:
    db = None

    def __init__(self, db) -> None:
        self.db = db

    def create_quiz(self, quiz_input, user):
        quiz_input.id = str(uuid.uuid1()) if quiz_input.id is None else quiz_input.id
        quiz_data = quiz_input.dict()
        if self.get_quiz(quiz_data["id"]):
            raise HTTPException(status_code=400, detail="quiz id already used ")
        quiz_data["owner"] = user["uid"]
        quiz_data["owner_email"] = user["email"]
        self.db.collection("quiz").document(quiz_data["id"]).set(quiz_data)
        return quiz_data

    def get_quiz(self, quiz_id):
        quiz = self.db.collection("quiz").document(quiz_id).get().to_dict()
        return quiz

    def get_quiz_or_error(self, quiz_id):
        quiz = self.get_quiz(quiz_id=quiz_id)
        if quiz is None:
            raise HTTPException(status_code=404, detail="quiz does not exist")
        return quiz

    def submit_answer(self, quiz_id, submitted_answers, user):
        quiz = self.get_quiz_or_error(quiz_id)
        self._validate_submitted_answers(submitted_answers, quiz)
        score = self._calculate_score(submitted_answers, quiz)
        self._update_score(user, quiz, score, submitted_answers)
        return score

    def _update_score(self, user, quiz, score, submitted_answers):
        answer_ref = (
            self.db.collection("quiz")
            .document(quiz["id"])
            .collection("answers")
            .document(user["uid"])
        )

        if answer_ref.get().exists:
            raise HTTPException(
                status_code=400, detail="already submitted answer cannot submit again"
            )

        self.db.collection("quiz").document(quiz["id"]).collection("answers").document(
            user["uid"]
        ).set(
            {
                "score": score,
                "id": user["uid"],
                "email": user["email"],
                "submitted_on": firestore.SERVER_TIMESTAMP,
                "submitted_answer": submitted_answers.dict()["answers"],
            }
        )

    def _calculate_score(self, submitted_answers, quiz):
        total_score = 0
        for question, ans in zip(quiz["questions"], submitted_answers.answers):
            if set(question["correct_options"]) == set(ans.selected_options):
                total_score += question["score"]
        return total_score

    def _validate_submitted_answers(self, submitted_answers, quiz):
        if len(submitted_answers.answers) != len(quiz["questions"]):
            raise HTTPException(
                status_code=400,
                detail=f"submitted {len(submitted_answers.answers)} answers instead of { len(quiz['questions'])} ",
            )

    def get_results(self, quiz_id):
        results = [
            e.to_dict()
            for e in self.db.collection("quiz")
            .document(quiz_id)
            .collection("answers")
            .stream()
        ]
        return results
