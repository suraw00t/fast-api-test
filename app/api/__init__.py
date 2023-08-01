import importlib
import pathlib
import os
import sys

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler


async def init_router(app, settings):
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    current_directory = pathlib.Path(__file__).parent
    routers = await get_subrouters(current_directory)
    # routers = await test_get_routers()

    # logger.debug(f"routers {routers}")
    for router in routers:
        # logger.debug(f"{router.tags}")
        app.include_router(router, prefix=f"{settings.API_PREFIX}", tags=router.tags)


async def get_subrouters(directory):
    routers = []

    package = directory.parts[len(pathlib.Path.cwd().parts) :]
    parent_router = None

    try:
        pymod_file = f"{'.'.join(package)}"
        pymod = importlib.import_module(pymod_file)

        if "router" in dir(pymod):
            parent_router = pymod.router
            routers.append(parent_router)
    except Exception as e:
        logger.exception(e)
        return routers

    subrouters = []
    for module in directory.iterdir():
        if "__" == module.name[:2]:
            continue

        if module.match("*.py"):
            try:
                pymod_file = f"{'.'.join(package)}.{module.stem}"
                pymod = importlib.import_module(pymod_file)

                if "router" in dir(pymod):
                    subrouters.append(pymod.router)
            except Exception as e:
                logger.exception(e)

        elif module.is_dir():
            subrouters.extend(await get_subrouters(module))

    for router in subrouters:
        logger.info(f"router {router} {router.prefix}")
        if parent_router:
            parent_router.include_router(router)
        else:
            routers.append(router)

    return routers


async def test_get_routers():
    routers = []
    sub_routers = []
    package = sys.modules[__name__].__package__
    py_file = package.replace(".", "/")
    for dirpath, _, filenames in os.walk(py_file):
        if dirpath.endswith("__"):
            continue

        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("__"):
                py_package = os.path.join(dirpath, filename[:-3]).replace("/", ".")
            else:
                py_package = dirpath.replace("/", ".")

            module = importlib.import_module(py_package)
            if hasattr(module, "router"):
                router = getattr(module, "router")
                if len(py_package.split(".")) == 3:
                    routers.append(router)
                else:
                    sub_routers.append(router)

                print(module.__name__, ":", py_package)

    return routers
