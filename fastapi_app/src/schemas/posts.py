from datetime import datetime
from pydantic import ConfigDict, BaseModel
from typing import Optional

from schemas.category import CategoryResponse
from schemas.location import LocationResponse
from models import Post


class PostRequest(Post):
    pass


class PostUpdate(BaseModel):
    is_published: bool | None = True
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    location_id: int | None = None
    category_id: int | None = None
    image: str | None = None


class PostResponse(Post):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    text: str
    pub_date: datetime
    author_id: int
    created_at: datetime

    category: Optional[CategoryResponse] = None
    location: Optional[LocationResponse] = None
