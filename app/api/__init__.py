import importlib
import pathlib


from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger
import os

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler


def init_router(app, settings):
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    current_directory = pathlib.Path(__file__).parent
    routers = get_subrouters(current_directory)
    # logger.debug(f"routers {routers}")

    for router in routers:
        logger.debug(f"{router.tags}")
        app.include_router(router, prefix=f"{settings.API_PREFIX}", tags=router.tags)


def get_subrouters(directory):
    routers = []
    subrouters = []
    package = directory.parts[len(pathlib.Path.cwd().parts) :]
    py_file = f"{'/'.join(package)}"

    for dirpath, _, filenames in os.walk(py_file):
        if dirpath.endswith("__"):
            continue

        parent_router = None
        for filename in sorted(filenames):
            pymod_dir = dirpath.replace("/", ".")
            if filename.endswith(".py"):
                if filename.startswith("__"):
                    pymod = importlib.import_module(pymod_dir)
                    if "router" in dir(pymod):
                        parent_router = pymod.router
                        subrouters.append(parent_router)

                if not filename.startswith("__"):
                    pymod = importlib.import_module(pymod_dir)
                    module_name = filename[:-3]
                    pymod_file = f"{pymod_dir}.{module_name}"
                    pymod = importlib.import_module(pymod_file)
                    if "router" in dir(pymod):
                        router = pymod.router
                        if parent_router:
                            parent_router.include_router(router)
                        else:
                            routers.append(router)

    for router in subrouters:
        routers.append(router)
        logger.debug(f"router {router} {router.prefix}")

    return routers
