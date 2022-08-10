from typing import List

from beanie import Document, PydanticObjectId

from .user import User


class Vote(Document):
    id: PydanticObjectId
    users: List[PydanticObjectId] = []

    class Settings:
        name = "votes"
