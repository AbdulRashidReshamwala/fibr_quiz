import uuid


class QuizService:
    db = None

    def __init__(self, db) -> None:
        self.db = db

    def create_quiz(self, quiz):
        quiz.id = str(uuid.uuid1()) if quiz.id is None else quiz.id
        self.db.collection("quiz").document(quiz.id).set(quiz.dict())

    