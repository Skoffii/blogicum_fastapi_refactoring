from pydantic import BaseModel, Field
from typing import Annotated

from .models import Location

class LocationRequest(Location):
    pass


class LocationUpdate(Location):
    is_published: bool | None
    name: Annotated[str | None, Field(max_length=256)] = None


class LocationResponse(Location):
    pass
