from pydantic import BaseModel, Field

from datetime import datetime


class Post(BaseModel):
    id: int
    is_published: bool = True
    created_at: datetime
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime
    image: str | None = None
    author_id: int
    location: int | None = None
    category: int | None = None


class Category(BaseModel):
    is_published: bool = True
    title: str = Field(..., max_length=256)
    slug: str
    description: str


class Location(BaseModel):
    is_published: bool = True
    name: str = Field(..., max_length=256)


class Comment(BaseModel):
    text: str
    post_id: int
    created_at: datetime
    author_id: int
