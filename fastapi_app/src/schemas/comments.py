from pydantic import BaseModel, ConfigDict
from datetime import datetime

from ..models import Comment


class CommentRequest(Comment):
    pass


class CommentUpdate(BaseModel):
    text: str | None = None


class CommentResponse(Comment):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
