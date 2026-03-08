from pydantic import BaseModel, Field
from typing import Annotated


class Category(BaseModel):
    is_published: bool = True
    title: str = Field(max_length=256)
    description: str


class CategoryRequest(Category):
    pass


class CategoryUpdate(BaseModel):
    title:  Annotated[str | None, Field(max_length=256)]
    description: str


class CategiryResponse(Category):
    pass
