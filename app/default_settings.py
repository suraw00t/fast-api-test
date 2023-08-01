from typing import List, Tuple
from pydantic_settings import BaseSettings
import logging
import os


class DefaultSettings(BaseSettings):
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "fastapi test"
    VERSION: str = "0.0.1"

    MONGODB_DB: str = "fastapitest_db"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""

    SECRET_KEY: str = "secret"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    API_PREFIX: str = "/api"

    ALLOWED_HOSTS: List[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    FILE_PATH: str = ""

    class Config:
        env_file = ".env" if "pro" in os.getenv("APP_ENV", "").lower() else ".env.dev"
