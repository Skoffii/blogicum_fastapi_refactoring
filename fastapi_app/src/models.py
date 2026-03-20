from pydantic import BaseModel, Field, SecretStr, EmailStr
from typing import Annotated

from datetime import datetime


class User(BaseModel):
    login: str
    password: SecretStr
    first_name: str = Annotated[str | None, Field(max_length=256)]
    last_name: str = Annotated[str | None, Field(max_length=256)]
    email: EmailStr = Annotated[str | None, Field(max_length=256)]


class Post(BaseModel):
    is_published: bool = True
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    author_id: int
    location: int | None = None
    category: int | None = None
    image: str | None = None


class Category(BaseModel):
    is_published: bool = True
    title: str = Field(max_length=256)
    slug: str
    description: str


class Location(BaseModel):
    is_published: bool = True
    name: str = Field(max_length=256)


class Comment(BaseModel):
    text: str
    post_id: int
    author_id: int
