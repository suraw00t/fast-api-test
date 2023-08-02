from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app import fastapi_app

router = APIRouter(tags=["hello"], prefix="/hello")


@router.get("/")
async def hello():
    content = f"""<body>
    <form action="{fastapi_app.app.url_path_for("create_file")}" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    <form action="{fastapi_app.app.url_path_for("create_upload_file")}" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
</body>"""
    return HTMLResponse(content=content)
