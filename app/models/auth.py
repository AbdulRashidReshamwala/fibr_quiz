from pydantic import BaseModel, SecretStr, EmailStr


class EmailPasswordInput(BaseModel):
    email: EmailStr
    password: SecretStr


class JWTOutput(BaseModel):
    jwt: str
