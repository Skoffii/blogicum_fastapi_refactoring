from pydantic import BaseModel, Field, field_validator, ConfigDict
import re


def valid_name(name: str):
    if name is None:
        return name
    if len(name) < 1 or len(name) > 256:
        raise ValueError(
            "Название локации должно быть длиннее 0 символов и короче 257 символов."
        )
    if re.search(r"<[a-z][\s\S]*>", name, re.IGNORECASE):
        raise ValueError("Название локации не должно содержать HTML-теги.")
    return name


class LocationBase(BaseModel):
    name: str = Field(...)
    is_published: bool = Field(default=True)

    @field_validator("name", mode="after")
    @staticmethod
    def check_name(name: str):
        return valid_name(name)


class LocationRequest(LocationBase):
    """Для создания локации"""

    pass


class LocationUpdate(BaseModel):
    name: str = Field(default=None)
    is_published: bool = Field(default=None)

    @field_validator("name", mode="after")
    @staticmethod
    def check_name(name: str):
        return valid_name(name)


class LocationResponse(BaseModel):
    id: int
    name: str
    is_published: bool

    model_config = ConfigDict(from_attributes=True)
