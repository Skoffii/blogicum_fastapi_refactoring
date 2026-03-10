from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    text: str
    post_id: int
    created_at: datetime
    author_id: int


class CommentRequest(BaseModel):
    pass


class CommentUpdate(BaseModel):
    post_id: int
    text: str | None = None
    author_id: int


class CommentResponse(Comment):
    pass
