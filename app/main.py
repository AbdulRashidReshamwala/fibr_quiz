import random
import string
import time
from fastapi import FastAPI, Request
from .routers import auth, quiz
from .config import settings
from .utils import setup_firebase
from fastapi.templating import Jinja2Templates
from loguru import logger


templates = Jinja2Templates(directory="app/templates")

app = FastAPI()


@app.get("/health", tags=["health_check"], name="Health Check")
def read_root() -> str:
    return {"msg": "Hello World"}


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting application in env : {settings.env}")
    setup_firebase()
    logger.info(f"Started application sucessfully")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


app.include_router(auth.router)
app.include_router(quiz.router)
