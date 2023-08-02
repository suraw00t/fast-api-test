from fastapi import APIRouter, UploadFile
from loguru import logger

router = APIRouter(prefix="/hen")


@router.get("/hen")
def hen():
    logger.debug("Hello world")
    return {"msg": "my hen eiei"}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
