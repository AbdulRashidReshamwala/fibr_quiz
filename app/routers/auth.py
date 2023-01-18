from fastapi import APIRouter, Depends, HTTPException
from firebase_admin._auth_utils import EmailAlreadyExistsError

from ..models.auth import EmailPasswordInput, JWTOutput
from ..services.auth import AuthService
from ..dependencies import get_auth_service, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/create")
def create_user(
    create_user_input: EmailPasswordInput,
    auth_service: AuthService = Depends(get_auth_service),
) -> JWTOutput:
    try:
        user = auth_service.create_user(
            email=create_user_input.email,
            password=create_user_input.password.get_secret_value(),
        )
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=400, detail="email already exist please sign in to continue"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="error createing user please try again later"
        )
    jwt = auth_service.create_jwt(user.uid)
    return JWTOutput(jwt=jwt)


@router.post("/me")
def login_user(
    user=Depends(get_current_user),
):
    return user
