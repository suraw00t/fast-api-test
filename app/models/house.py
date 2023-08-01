from typing import List

from beanie import Document, Link, Indexed, PydanticObjectId
import typing as t
from .fields import FileDocument
from bson import DBRef, ObjectId


class WindowAPI(Document):
    x: t.Optional[int]
    y: t.Optional[int]

    class Settings:
        name = "windows"


class DoorAPI(Document):
    t: int = 10

    class Settings:
        name = "doors"


class RoofAPI(Document):
    r: int = 100

    class Settings:
        name = "roof"


class HouseAPI(Document):
    windows: List[Link[WindowAPI]]
    name: Indexed(str)
    height: int = 2

    class Settings:
        name = "houses"


class Picture(Document):
    file: PydanticObjectId

    class Settings:
        name = "pictures"
        # use_state_management = True
        # state_management_save_previous = True

    # class Config:
    #     arbitrary_types_allowed = True
