from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix="/hen")


@router.get("/hen")
def hen():
    logger.debug("Hello world")
    return {"msg": "my hen eiei"}
