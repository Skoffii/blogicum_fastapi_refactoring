from infrastructure.database import database
from infrastructure.repos.user_rep import UserRepository
from schemas.users import UserResponse, UserUpdate, UserRequest
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.get_by_id(session=session, user_id=user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserResponse.model_validate(obj=user)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.get_by_login(session=session, login=login)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserResponse.model_validate(obj=user)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequest) -> UserResponse:
        with self._database.session() as session:
            existing_user = self._repo.get_by_login(
                session=session, login=data.username
            )

            if existing_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
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
            user = self._repo.get_by_id(session=session, user_id=user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            user = self._repo.update_user(session=session, user=user, data=data)
        return UserResponse.model_validate(obj=user)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            user = self._repo.get_by_id(session=session, user_id=user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if current_user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            self._repo.delete_user(session=session, user=user)
