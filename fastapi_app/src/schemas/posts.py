from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime as datetime
from typing import List, Optional
import re


def valid_title(title: str):
    if title is None:
        return title
    len_title = len(title)
    if len_title < 5 or len_title > 40:
        raise ValueError(
            'Заголовок поста должен быть длиннее 4 символов и короче 41 символа.'
        )
    if re.search(r'<[a-z][\s\S]*>', title, re.IGNORECASE):
        raise ValueError(
            'Заголовок не должен содержать HTML-теги.'
        )
    return title


def valid_text(text: str):
    if text is None:
        return text
    if len(text) < 1:
        raise ValueError(
            'Текст поста не может быть пустым.'
        )
    if len(text) > 10000:
        raise ValueError(
            'Текст поста должен быть короче 10001 символа.'
        )
    return text


def valid_slug(slug: str):
    if slug is None:
        return slug
    if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
        raise ValueError(
            'Slug может содержать только латиницу, цифры, дефис и подчёркивание.'
        )
    return slug.lower()


class PostBase(BaseModel):
    title: str = Field(...)
    text: str = Field(...)
    is_published: bool = Field(default=True)
    image: str | None = Field(default=None)

    @field_validator("title", mode="after")
    @staticmethod
    def check_title(title: str):
        return valid_title(title)

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)


class PostRequest(PostBase):
    pub_date: Optional[datetime] = Field(default=None)
    location_name: str | None = Field(default=None)
    category_slug: str | None = Field(default=None)

    @field_validator("category_slug", mode="after")
    @staticmethod
    def check_category_slug(category_slug: str | None):
        return valid_slug(category_slug)


class PostUpdate(BaseModel):
    title: str = Field(default=None)
    text: str = Field(default=None)
    pub_date: Optional[datetime] = Field(default=None)
    is_published: bool = Field(default=None)
    image: str = Field(default=None)
    location_name: str | None = Field(default=None)
    category_slug: str | None = Field(default=None)

    @field_validator("title", mode="after")
    @staticmethod
    def check_title(title: str):
        return valid_title(title)

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        return valid_text(text)

    @field_validator("category_slug", mode="after")
    @staticmethod
    def check_category_slug(category_slug: str | None):
        return valid_slug(category_slug)


class PostResponse(BaseModel):
    id: int
    created_at: datetime
    title: str = Field(default=None)
    text: str = Field(default=None)
    pub_date: Optional[datetime] = Field(default=None)
    is_published: bool = Field(default=None)
    image: str | None = Field(default=None)
    location_id: int | None = Field(default=None)
    category_id: int | None = Field(default=None)
    author_id: int = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("title", mode="after")
    @staticmethod
    def check_title(title: str):
        return valid_title(title)