from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings
from infrastructure.database import database
from infrastructure.repos.user_rep import UserRepository
from schemas.users import UserResponse
from core.exceptions.domain_exceptions import (
    InvalidUsernameException,
    WrongPasswordException,
)
from core.exceptions.infrastructure_exceptions import UserNotFoundByUsername
from resourses.auth import verify_password
import logging

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str, password: str) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_login(session=session, login=username)
        except UserNotFoundByUsername:
            error = InvalidUsernameException(username=username)
            logger.error(error.get_detail())
            raise error
        if not verify_password(plain_password=password, hashed_password=user.password):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error
        return UserResponse.model_validate(obj=user)


class CreateAccessTokenUseCase:
    async def execute(self, login: str, expires_delta: timedelta | None = None) -> str:
        to_encode = {"sub": login}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithm=settings.AUTH_ALGORITHM,
        )
        return encoded_jwt
