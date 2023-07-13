from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix="/house")


@router.get("/do")
def house():
    logger.debug("Hello world")
    return {"msg": "my home eiei"}
