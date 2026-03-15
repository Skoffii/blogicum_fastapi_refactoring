from datetime import datetime
from pydantic import ConfigDict, BaseModel

from ..models import Post


class PostRequest(Post):
    pass


class PostUpdate(BaseModel):
    is_published: bool | None = True
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    location: int | None = None
    category: int | None = None
    image: str | None = None


class PostResponse(Post):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    text: str
    pub_date: datetime
    author_id: int
    location: int | None = None
    category: int | None = None
    created_at: datetime
