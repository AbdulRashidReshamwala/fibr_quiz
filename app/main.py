from fastapi import FastAPI
from .routers import auth, quiz

app = FastAPI()


@app.get("/", tags=["health_check"], name="Health Check")
def read_root() -> str:
    return "Hello World"


@app.on_event("startup")
async def startup_event():
    print("Starting application")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application")


app.include_router(auth.router)
app.include_router(quiz.router)
