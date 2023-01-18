import uuid

from fastapi import HTTPException


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
