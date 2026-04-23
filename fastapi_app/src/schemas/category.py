from pydantic import BaseModel, Field, field_validator, ConfigDict
import re


def valid_title(title: str):
    if title is None:
        return title
    if len(title) < 1 or len(title) > 256:
        raise ValueError(
            'Название категории должно быть длиннее 0 символов и короче 257 символов.'
        )
    return title


def valid_slug(slug: str):
    if slug is None:
        return slug
    if len(slug) < 1 or len(slug) > 200:
        raise ValueError(
            'Slug должен быть длиннее 0 символов и короче 201 символа.'
        )
    if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
        raise ValueError(
            'Slug может содержать только латиницу, цифры, дефис и подчёркивание.'
        )
    return slug.lower()


def valid_description(description: str):
    if description is None:
        return description
    if len(description) < 1:
        raise ValueError(
            'Описание категории не может быть пустым.'
        )
    if len(description) > 1000:
        raise ValueError(
            'Описание категории должно быть короче 1001 символа.'
        )
    return description


class CategoryBase(BaseModel):
    title: str = Field(...)
    slug: str = Field(...)
    description: str = Field(...)
    is_published: bool = Field(default=True)

    @field_validator("title", mode="after")
    @staticmethod
    def check_title(title: str):
        return valid_title(title)

    @field_validator("slug", mode="after")
    @staticmethod
    def check_slug(slug: str):
        return valid_slug(slug)

    @field_validator("description", mode="after")
    @staticmethod
    def check_description(description: str):
        return valid_description(description)


class CategoryRequest(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str = Field(default=None)
    slug: str = Field(default=None)
    description: str = Field(default=None)
    is_published: bool = Field(default=None)

    @field_validator("title", mode="after")
    @staticmethod
    def check_title(title: str):
        return valid_title(title)

    @field_validator("slug", mode="after")
    @staticmethod
    def check_slug(slug: str):
        return valid_slug(slug)

    @field_validator("description", mode="after")
    @staticmethod
    def check_description(description: str):
        return valid_description(description)


class CategoryResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    is_published: bool

    model_config = ConfigDict(from_attributes=True)