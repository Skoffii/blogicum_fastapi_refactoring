from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime as datetime
import re


def valid_text(text: str):
    if text is None:
        return text
    if len(text) < 1:
        raise ValueError("Текст комментария не может быть пустым.")
    if len(text) > 1000:
        raise ValueError("Текст комментария должен быть короче 1001 символа.")
    if re.search(r"<[a-z][\s\S]*>", text, re.IGNORECASE):
        raise ValueError("Текст комментария не должен содержать HTML-теги.")
    return text


class CommentBase(BaseModel):
    text: str = Field(...)
    image: str

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)


class CommentRequest(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: str = Field(default=None)
    image: str

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)


class CommentResponse(BaseModel):
    id: int
    text: str
    image: str
    author_id: int
    created_at: datetime
    post_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentImageResponse(BaseModel):
    image: str
