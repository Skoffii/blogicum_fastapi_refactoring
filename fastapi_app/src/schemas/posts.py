from pydantic import BaseModel
from datetime import datetime

from location import Location
from category import Category


class Post(BaseModel):
    is_published: bool = True
    created_at: datetime
    title: str
    text: str
    pub_date: datetime
    image: str | None = None
    author_id: int
    location: Location | None = None
    category: Category | None = None


class PostRequest(Post):
    pass


class PostUpdate(Post):
    is_published: bool | None = True
    created_at: datetime | None = None
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    image: str | None = None
    location: Location | None = None
    category: Category | None = None


class PostResponse(BaseModel):
    author: int
    title: str
    created_at: datetime
    location: Location | None = None
    category: Category | None = None
