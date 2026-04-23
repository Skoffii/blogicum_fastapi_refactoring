from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime as datetime
import re


def valid_text(text: str):
    if text is None:
        return text
    if len(text) < 1:
        raise ValueError(
            'Текст комментария не может быть пустым.'
        )
    if len(text) > 1000:
        raise ValueError(
            'Текст комментария должен быть короче 1001 символа.'
        )
    if re.search(r'<[a-z][\s\S]*>', text, re.IGNORECASE):
        raise ValueError(
            'Текст комментария не должен содержать HTML-теги.'
        )
    return text


def valid_username(username: str):
    if username is None:
        return username
    if len(username) < 3 or len(username) > 20:
        raise ValueError(
            'Имя пользователя должно быть длиннее 2 символов и короче 21 символа.'
        )
    return username.lower()


class CommentBase(BaseModel):
    text: str = Field(...)

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)


class CommentRequest(CommentBase):
    post_id: int = Field(...)


class CommentUpdate(BaseModel):
    text: str = Field(default=None)

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)


class CommentResponse(BaseModel):
    id: int
    text: str
    author_username: str
    created_at: datetime
    post_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("author_username", mode="after")
    @staticmethod
    def check_username(author_username: str):
        return valid_username(author_username)