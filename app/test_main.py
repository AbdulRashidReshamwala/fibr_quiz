from fastapi.testclient import TestClient
from dotenv import load_dotenv
from .main import app
from .dependencies import get_auth_provider
from .utils import setup_firebase

import pyrebase

config = {
    "apiKey": "AIzaSyAQ03c_-i5bOpyvY3_wyqubeDcJ0EwAUuc",
    "authDomain": "fibr-quiz.firebaseapp.com",
    "projectId": "fibr-quiz",
    "storageBucket": "fibr-quiz.appspot.com",
    "messagingSenderId": "968443519261",
    "appId": "1:968443519261:web:30528f2b6b79b72eac81f4",
    "databaseURL": "",
}


load_dotenv()
setup_firebase()
client = TestClient(app)


firebase = pyrebase.initialize_app(config)
client_auth = firebase.auth()


def get_jwt(uid):
    auth = get_auth_provider()
    id_token = auth.create_custom_token(uid).decode()
    tokens = client_auth.sign_in_with_custom_token(id_token)
    return tokens["idToken"]


def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_auth_me_endpoint_success():
    TEST_UID = "hxrBP48MN1RiX516Hw8Ha7nBMjR2"
    jwt = get_jwt(TEST_UID)
    response = client.post("/auth/me", headers={"auth": jwt})
    assert response.status_code == 200


def test_auth_me_endpoint_fail():
    FAKE_ID_TOKEN = "TEST_TOKEN"
    response = client.post("/auth/me", headers={"auth": FAKE_ID_TOKEN})
    assert response.status_code == 401


def test_login_page_success():
    response = client.get("/")
    assert response.status_code == 200


def test_create_quiz_success():
    TEST_UID = "hxrBP48MN1RiX516Hw8Ha7nBMjR2"
    jwt = get_jwt(TEST_UID)
    response = client.post(
        "/quiz/create",
        headers={"auth": jwt},
        json={
            "title": "string",
            "questions": [
                {
                    "question": "string",
                    "options": ["string"],
                    "correct_options": [0],
                    "score": 10,
                }
            ],
        },
    )
    assert response.status_code == 200


def test_create_quiz_duplicate_id_failure():
    TEST_UID = "hxrBP48MN1RiX516Hw8Ha7nBMjR2"
    jwt = get_jwt(TEST_UID)
    response = client.post(
        "/quiz/create",
        headers={"auth": jwt},
        json={
            "id": "string",
            "title": "string",
            "questions": [
                {
                    "question": "string",
                    "options": ["string"],
                    "correct_options": [0],
                    "score": 10,
                }
            ],
        },
    )
    assert response.status_code == 400


# only allow authenticated users to view quiz
def test_get_quiz_failure():
    FAKE_ID_TOKEN = "TEST_TOKEN"
    response = client.get("/quiz/get/test", headers={"auth": FAKE_ID_TOKEN})
    assert response.status_code == 401


def test_get_quiz_success():
    TEST_UID = "hxrBP48MN1RiX516Hw8Ha7nBMjR2"
    jwt = get_jwt(TEST_UID)
    response = client.get("/quiz/get/test", headers={"auth": jwt})
    assert response.status_code == 200


def test_get_quiz_result_success():
    TEST_UID = "hxrBP48MN1RiX516Hw8Ha7nBMjR2"
    jwt = get_jwt(TEST_UID)
    response = client.get("quiz/results/test", headers={"auth": jwt})
    assert response.status_code == 200


# only owner should be allowed to view results
def test_get_quiz_result_fail():
    TEST_UID_FAIL = "hEaHxebAooTlRGujcdk7Ik8ZGku1"
    jwt = get_jwt(TEST_UID_FAIL)
    response = client.get("quiz/results/test", headers={"auth": jwt})
    assert response.status_code == 401
