from pydantic import Field, BaseModel, ConfigDict
from typing import Annotated

from models import Category


class CategoryRequest(Category):
    pass


class CategoryUpdate(BaseModel):
    title: Annotated[str | None, Field(max_length=256)]
    description: str | None


class CategoryResponse(Category):
    model_config = ConfigDict(from_attributes=True)
    id: int
