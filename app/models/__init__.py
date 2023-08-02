import sys
import inspect
import beanie
import typing as t
from loguru import logger
from beanie.odm.documents import DocType
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from app.core.settings.app import AppSettings
from .articles import TestDrivenArticle
from .house import HouseAPI, WindowAPI, Picture, RoofAPI, DoorAPI

__all__ = [
    "TestDrivenArticle",
    "HouseAPI",
    "WindowAPI",
    "Picture",
    "RoofAPI",
    "DoorAPI",
]


# async def get_model_modules() -> list:
#     import pathlib, os, importlib

#     modules = []
#     current_directory = pathlib.Path(__file__).parent
#     package = current_directory.parts[len(pathlib.Path.cwd().parts) :]
#     py_file = f"{'/'.join(package)}"
#     for dirpath, _, filenames in os.walk(py_file):
#         if dirpath.endswith("__"):
#             continue

#         pymod_dir = dirpath.replace("/", ".")
#         for filename in filenames:
#             if filename.endswith(".py") and filename != "__init__.py":
#                 module_name = filename[:-3]
#                 pymod_file = f"{pymod_dir}.{module_name}"
#                 for _, cls in inspect.getmembers(
#                     importlib.import_module(pymod_file), inspect.isclass
#                 ):
#                     if (
#                         cls.__module__ == pymod_file
#                         and beanie.Document in cls.__bases__
#                     ):
#                         modules.append(cls)

#     logger.debug("beanie models >> " + str(modules))
#     return modules


async def gather_documents() -> t.Sequence[t.Type[DocType]]:
    """Returns a list of all MongoDB document models defined in `models` module."""
    return [
        doc
        for _, doc in inspect.getmembers(sys.modules[__name__], inspect.isclass)
        if issubclass(doc, beanie.Document) and doc.__name__ != "Document"
    ]


class BeanieClient:
    async def init_beanie(self, settings: AppSettings):
        url = "{}{}".format(
            settings.MONGODB_URI
            if settings.MONGODB_URI.endswith("/")
            else settings.MONGODB_URI + "/",
            settings.MONGODB_DB,
        )
        logger.info(url)
        self.client = AsyncIOMotorClient(url)
        self.database = self.client.beanie_db

        try:
            await beanie.init_beanie(
                self.database,
                document_models=await gather_documents(),
            )
        except Exception as e:
            logger.error(e)


beanie_client = BeanieClient()
