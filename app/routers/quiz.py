from fastapi import APIRouter


router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.post("/create")
def ceate_quiz():
    pass
