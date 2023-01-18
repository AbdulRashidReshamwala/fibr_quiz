from typing import Union
from fastapi import Depends, HTTPException, Header
from firebase_admin import firestore, auth

from app.services.auth import AuthService

from .services.quiz import QuizService


def get_db_provider():
    db = firestore.client()
    try:
        yield db
    finally:
        pass
    return db


def get_quiz_service():
    quiz_service = QuizService(db=next(get_db_provider()))
    return quiz_service


def get_auth_provider():
    return auth


def get_auth_service():
    auth_service = AuthService(auth_provider=get_auth_provider())
    return auth_service


def get_auth_token(auth: Union[str, None] = Header(default=None)):
    if auth is None:
        raise HTTPException(status_code=401, detail="no authorization header found")
    return auth


def get_current_user(
    token: str = Depends(get_auth_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = auth_service.verify_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="error verifying token")
    return user
