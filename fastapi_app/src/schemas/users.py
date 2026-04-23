from pydantic import BaseModel, Field, field_validator, SecretStr, EmailStr, ConfigDict
from typing import Annotated, Optional
import re


def valid_username(username: str):
    if len(username) < 3 or len(username) > 20:
        raise ValueError(
            'Имя пользователя должно быть длиннее 2 символов и короче 21 символа.'
        )
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError(
            'Имя пользователя может содержать только латиницу, цифры и подчёркивание.'
        )
    return username.lower()


def valid_password(password: str):
    if len(password) < 8 or len(password) > 72:
        raise ValueError(
            'Пароль должен быть длиннее 7 символов и короче 73 символов.'
        )
    if not re.search(r'[A-Za-z]', password):
        raise ValueError(
            'Пароль должен содержать хотя бы одну букву.'
        )
    if not re.search(r'\d', password):
        raise ValueError(
            'Пароль должен содержать хотя бы одну цифру.'
        )
    return password


def valid_name(name: str | None):
    if name is None:
        return name
    if len(name) > 256:
        raise ValueError(
            'Имя или фамилия должны быть короче 257 символов.'
        )
    if re.search(r'<[a-z][\s\S]*>', name, re.IGNORECASE):
        raise ValueError(
            'Имя или фамилия не должны содержать HTML-теги.'
        )
    return name


def valid_email(email: str | None):
    if email is None:
        return email
    if len(email) > 254:
        raise ValueError(
            'Email должен быть короче 255 символов.'
        )
    return email.lower()


class UserBase(BaseModel):
    username: str = Field(...)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

    @field_validator("first_name", mode="after")
    @staticmethod
    def check_first_name(first_name: str | None) -> str | None:
        return valid_name(first_name)

    @field_validator("last_name", mode="after")
    @staticmethod
    def check_last_name(last_name: str | None) -> str | None:
        return valid_name(last_name)

    @field_validator("email", mode="after")
    @staticmethod
    def check_email(email: Optional[EmailStr]):
        return valid_email(email)


class UserRequest(UserBase):
    password: SecretStr = Field(...)

    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: SecretStr):
        return valid_password(password.get_secret_value())


class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(default=None, max_length=256)] = None
    last_name: Annotated[str | None, Field(default=None, max_length=256)] = None
    email: Optional[EmailStr] = Field(default=None, max_length=254)

    @field_validator("first_name", mode="after")
    @staticmethod
    def check_first_name(first_name: str | None) -> str | None:
        return valid_name(first_name)

    @field_validator("last_name", mode="after")
    @staticmethod
    def check_last_name(last_name: str | None) -> str | None:
        return valid_name(last_name)

    @field_validator("email", mode="after")
    @staticmethod
    def check_email(email: Optional[EmailStr]):
        return valid_email(email)


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("username", mode="after")
    @staticmethod
    def check_username(username: str) -> str:
        return valid_username(username)

    @field_validator("first_name", mode="after")
    @staticmethod
    def check_first_name(first_name: str | None) -> str | None:
        return valid_name(first_name)

    @field_validator("last_name", mode="after")
    @staticmethod
    def check_last_name(last_name: str | None) -> str | None:
        return valid_name(last_name)

    @field_validator("email", mode="after")
    @staticmethod
    def check_email(email: str | None) -> str | None:
        return valid_email(email)