from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fibr Quiz"
    env: str = "production"

    class Config:
        env_file = ".env"


settings = Settings()
