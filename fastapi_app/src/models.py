from pydantic import BaseModel, Field, SecretStr, EmailStr
from typing import Annotated, Optional


class User(BaseModel):
    password: SecretStr = Field(min_length=8, max_length=72)
    username: str
    last_name: str = Annotated[str | None, Field(max_length=256)]
    email: Optional[EmailStr] = Field(None, max_length=254)
    first_name: str = Annotated[str | None, Field(max_length=256)]


class Post(BaseModel):
    is_published: bool = True
    title: str = Field(max_length=256)
    text: str
    location_id: int | None = None
    category_id: int | None = None
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
