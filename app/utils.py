import firebase_admin
from firebase_admin import credentials
from .config import settings


def setup_firebase():
    firebase_admin.initialize_app()
