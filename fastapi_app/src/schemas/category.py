from pydantic import BaseModel, Field
from typing import Annotated

from .models import Category


class Category(BaseModel):
    is_published: bool = True
    title: str = Field(max_length=256)
    slug: str
    description: str


class CategoryRequest(Category):
    pass


class CategoryUpdate(BaseModel):
    title: Annotated[str | None, Field(max_length=256)]
    description: str


class CategoryResponse(Category):
    pass
