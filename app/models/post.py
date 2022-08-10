from datetime import datetime
from typing import Optional

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field

from .user import RefUser, User


class Post(Document):
    tweet: str
    published: bool = True
    owner: Link[User]
    votes: int = 0
    created_at: datetime = datetime.now()

    class Settings:
        name = "posts"


class CreatePost(BaseModel):
    tweet: str
    published: bool = True


class UpdatePost(BaseModel):
    tweet: Optional[str]
    published: Optional[bool]


class OutPost(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    tweet: str
    published: bool
    owner: RefUser
    votes: int
    created_at: datetime
