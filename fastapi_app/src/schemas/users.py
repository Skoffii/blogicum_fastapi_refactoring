from pydantic import BaseModel, SecretStr, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
