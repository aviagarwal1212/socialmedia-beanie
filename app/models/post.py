from ast import alias
from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Post(Document):
    tweet: str
    published: bool = True
    owner_id: PydanticObjectId
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
    owner_id: PydanticObjectId
    created_at: datetime
