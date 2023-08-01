import os
import pathlib
import inspect
import importlib
import beanie

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from loguru import logger
from .articles import TestDrivenArticle
from .house import HouseAPI, WindowAPI, Picture
from app.core.settings.app import AppSettings

__all__ = ["TestDrivenArticle", "HouseAPI", "WindowAPI", "Picture"]


async def get_model_modules() -> list:
    classes = []
    current_directory = pathlib.Path(__file__).parent
    package = current_directory.parts[len(pathlib.Path.cwd().parts) :]
    py_file = f"{'/'.join(package)}"
    for dirpath, _, filenames in os.walk(py_file):
        if dirpath.endswith("__"):
            continue

        pymod_dir = dirpath.replace("/", ".")
        for filename in filenames:
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                pymod_file = f"{pymod_dir}.{module_name}"
                for _, cls in inspect.getmembers(
                    importlib.import_module(pymod_file), inspect.isclass
                ):
                    if (
                        cls.__module__ == pymod_file
                        and beanie.Document in cls.__bases__
                    ):
                        classes.append(cls)

    logger.debug("beanie models >> " + str(classes))
    return classes


async def init_beanie(settings: AppSettings) -> AsyncIOMotorClient:
    url = "{}/{}".format(settings.MONGODB_URI, settings.MONGODB_DB)
    logger.debug(url)
    client = AsyncIOMotorClient(url)

    try:
        await beanie.init_beanie(
            client.beanie_db,
            document_models=await get_model_modules(),
        )
    except Exception as e:
        logger.error(e)
