from fastapi import FastAPI, Request
from .routers import auth, quiz
from .config import settings
from .utils import setup_firebase
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()


@app.get("/health", tags=["health_check"], name="Health Check")
def read_root() -> str:
    return "Hello World 2"


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
