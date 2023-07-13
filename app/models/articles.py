from beanie import Document
import datetime


class TestDrivenArticle(Document):
    title: str
    content: str
    date: datetime.datetime
    author: str

    class Settings:
        name = "testdriven_collection"
