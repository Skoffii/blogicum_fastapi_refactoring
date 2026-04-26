from typing import Annotated
from fastapi import Depends
from jose import JWTError
from core.security import oauth2_scheme
from core.config import settings
from infrastructure.database import database
from infrastructure.repos.user_rep import UserRepository
from schemas.users import UserResponse


class CredentialsException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserResponse:
        _AUTH_MSG = "Невозможно проверить данные авторизации"
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException(_AUTH_MSG)
        except JWTError:
            raise CredentialsException(_AUTH_MSG)

        try:
            with database.session() as session:
                user = UserRepository().get_by_login(session=session, login=username)
        except Exception:
            raise CredentialsException(_AUTH_MSG)

        return UserResponse.model_validate(user)
