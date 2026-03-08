from pydantic import BaseModel, SecretStr, ConfigDict


class User(BaseModel):
    id: int
    login: str
    first_name: str | None = None
    email: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: SecretStr
