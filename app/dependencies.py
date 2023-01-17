from firebase_admin import firestore

from .services.quiz import QuizService


def get_firstore_db():
    db = firestore.client()
    try:
        yield db
    finally:
        pass
    return db


def get_quiz_service():
    quiz_service = QuizService(db=next(get_firstore_db()))
    return quiz_service
