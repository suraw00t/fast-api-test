from functools import lru_cache
from typing import Dict, Type

from app.core.settings.app import AppSettings


@lru_cache
def get_app_settings() -> AppSettings:
    config = AppSettings()
    return config
