from ast import alias
from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

    class Settings:
        name = "users"


class OutUser(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    email: EmailStr
    created_at: datetime


class RefUser(BaseModel):
    email: EmailStr
