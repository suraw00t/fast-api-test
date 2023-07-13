import beanie
from motor import motor_asyncio
from loguru import logger

__all__ = ["TestDrivenArticle", "HouseAPI"]


async def get_model_modules():
    import os
    import pathlib
    import inspect
    import importlib

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
                for name, cls in inspect.getmembers(
                    importlib.import_module(pymod_file), inspect.isclass
                ):
                    if cls.__module__ == pymod_file:
                        classes.append(cls)
    logger.debug("models " + str(classes))
    return classes


async def init_beanie(settings):
    url = "mongodb://{}:{}/{}".format(
        settings.MONGODB_HOST, settings.MONGODB_PORT, settings.MONGODB_DB
    )
    logger.debug(url)
    client = motor_asyncio.AsyncIOMotorClient(url)
    await beanie.init_beanie(
        client.beanie_db,
        document_models=await get_model_modules(),
    )
