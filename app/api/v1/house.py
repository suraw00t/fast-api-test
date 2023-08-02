from fastapi import APIRouter, File, UploadFile, FastAPI
from fastapi.responses import HTMLResponse
from loguru import logger
from app import models
import typing as t
from app import fastapi

root_router = fastapi.app
router = APIRouter(prefix="/house")


@router.get("/do")
async def house():
    logger.debug("Hello world")
    return {"msg": "my home eiei"}


@router.post("/windows")
async def create_windows(x: int, y: int):
    window = models.WindowAPI(x=x, y=y)
    await window.save()
    # logger.debug(window.x)
    # logger.debug(window.y)
    return window


@router.get("/find_window", response_model=t.List[models.WindowAPI])
async def find_windows(x: int = None, y: int = None):
    window_model = models.WindowAPI.find()
    if x is not None:
        window_model = window_model.find(models.WindowAPI.x == x)
    if y is not None:
        window_model = window_model.find(models.WindowAPI.y == y)

    windows = await window_model.to_list()

    return windows


@router.put("/update_window", response_model=models.WindowAPI)
async def update_window(id: str):
    window = await models.WindowAPI.get(id)
    logger.debug(window)
    return window


@router.post("/picture/")
async def upload_picture(file: t.Annotated[bytes, File()] = None):
    # data = models.Picture(file=file)
    from app.core.config import get_app_settings

    settings = get_app_settings()
    from PIL import Image

    from app.models import beanie_client

    print(beanie_client.database)
    image = Image.open(settings.FILE_PATH)
    width, height = image.size
    image_format = image.format
    print(f"Image Format: {image_format}")
    print(f"Image Size: {width}x{height}")


@router.post("/files/")
async def create_file(file: t.Annotated[bytes | None, File(description="Now here")]):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@router.get("/")
async def main():
    content = f"""<body>
    <form action="{root_router.url_path_for("create_file")}" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    <form action="{root_router.url_path_for("create_upload_file")}" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
</body>"""
    return HTMLResponse(content=content)
