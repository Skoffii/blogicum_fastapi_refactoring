from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    id: int
    is_published: bool = True
    created_at: datetime
    title: str
    text: str
    pub_date: datetime
    image: str | None = None
    author_id: int
    location: int | None = None
    category: int | None = None


class PostRequest(Post):
    pass


class PostUpdate(BaseModel):
    is_published: bool | None = True
    created_at: datetime | None = None
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    image: str | None = None
    location: int | None = None
    category: int | None = None


class PostResponse(BaseModel):
    id: int
    author: int
    title: str
    created_at: datetime
    location: int | None = None
    category: int | None = None
