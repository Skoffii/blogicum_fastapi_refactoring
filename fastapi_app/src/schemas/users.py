from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, Optional

from models import User


class UserUpdate(BaseModel):
    first_name: str = Annotated[str | None, Field(max_length=256)]
    last_name: str = Annotated[str | None, Field(max_length=256)]
    email: Optional[EmailStr] = Field(None, max_length=254)


class UserRequest(User):
    pass


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)
