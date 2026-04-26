from pydantic import Field, BaseModel

from resourses.field_description import ACCESS_TOKEN, TOKEN_TYPE, USERNAME


class Token(BaseModel):
    access_token: str = Field(description=ACCESS_TOKEN)
    token_type: str = Field(description=TOKEN_TYPE)


class UserData(BaseModel):
    user_id: int
    username: str
