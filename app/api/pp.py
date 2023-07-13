from fastapi import APIRouter

router = APIRouter(tags=["pp"], prefix="/pp")


@router.get("/")
def pp():
    return {"p": "pp"}
