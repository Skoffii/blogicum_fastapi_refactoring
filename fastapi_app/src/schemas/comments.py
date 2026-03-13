from pydantic import BaseModel
from datetime import datetime

from .models import Comment


class CommentRequest(Comment):
    pass


class CommentUpdate(Comment):
    text: str | None = None


class CommentResponse(Comment):
    pass
