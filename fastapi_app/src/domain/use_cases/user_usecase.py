from infrastructure.database import database
from infrastructure.repos.user_rep import UserRepository
from schemas.users import UserResponse, UserUpdate, UserRequest
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *

from passlib.context import CryptContext
from datetime import datetime

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session=session, user_id=user_id)
        except UserNotFoundById:
            raise UserNotFoundByIdException(user_id=user_id)

        return UserResponse.model_validate(obj=user)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_login(session=session, login=login)
        except UserNotFoundByUsername:
            raise UserNotFoundByUsernameException(username=login)

        return UserResponse.model_validate(obj=user)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequest) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.get_by_login(
                    session=session, login=data.username
                )
            except UserAlreadyExist:
                raise UserAlreadyExistExeption(username=data.username)
            except UserNotFoundByUsername:
                pass
            if data.email:
                existing_email = session.query(self._repo._model).where(self._repo._model.email == data.email).scalar()
                if existing_email:
                    raise UserEmailIsNotUniqueException(user_email=data.email)

        hash_pwd = pwd.hash(data.password.get_secret_value())
        user = self._repo.create_user(
            session=session,
            username=data.username,
            password=hash_pwd,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            is_staff=False,
            is_superuser=False,
            is_active=True,
            last_login=None,
            date_joined=datetime.now(),
        )
        return UserResponse.model_validate(obj=user)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, data: UserUpdate) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.get_by_id(session=session, user_id=user_id)
            except UserDoesNotExist:
                raise UserNotFoundByIdException(user_id=user_id)
            if data.email and data.email != user.email:
                existing_email = session.query(self._repo._model).where(self._repo._model.email == data.email).scalar()
                if existing_email:
                    raise UserEmailIsNotUniqueException(user_email=data.email)
            user = self._repo.update_user(session=session, user=user, data=data)
        return UserResponse.model_validate(obj=user)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            try:
                user = self._repo.get_by_id(session=session, user_id=user_id)
                if current_user_id != user_id:
                    raise UserPermissionDenied
            except UserPermissionDenied:
                raise UserPermisionException(current_user_id=current_user_id)
            self._repo.delete_user(session=session, user=user)
