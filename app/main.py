from fastapi import FastAPI
from .routers import auth, quiz
from .config import settings
from .utils import setup_firebase


app = FastAPI()


@app.get("/", tags=["health_check"], name="Health Check")
def read_root() -> str:
    return "Hello World 2"


@app.on_event("startup")
async def startup_event():
    print(f"Starting application in env : {settings.env}")
    setup_firebase()
    print(f"Started application sucessfully")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application")


app.include_router(auth.router)
app.include_router(quiz.router)
