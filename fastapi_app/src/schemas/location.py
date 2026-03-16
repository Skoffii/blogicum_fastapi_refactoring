from pydantic import Field, BaseModel, ConfigDict
from typing import Annotated

from models import Location


class LocationRequest(Location):
    pass


class LocationUpdate(BaseModel):
    is_published: bool | None
    name: Annotated[str | None, Field(max_length=256)] = None


class LocationResponse(Location):
    model_config = ConfigDict(from_attributes=True)
    id: int
