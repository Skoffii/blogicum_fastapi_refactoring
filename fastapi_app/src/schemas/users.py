from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from typing import Annotated

from models import User


class UserUpdate(BaseModel):
    first_name: str = Annotated[str | None, Field(max_length=256)]
    last_name: str = Annotated[str | None, Field(max_length=256)]
    email: EmailStr = Annotated[str | None, Field(max_length=256)]


class UserRequest(User):
    login: str
    password: SecretStr


class UserResponse(User):
    id: int
    login: str

    model_config = ConfigDict(from_attributes=True)
