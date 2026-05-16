from infrastructure.database import database
from infrastructure.repos.user_rep import UserRepository
from schemas.users import UserResponse, UserUpdate, UserRequest
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *
from sqlalchemy import select
import logging


logger = logging.getLogger(__name__)


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponse:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_id(session=session, user_id=user_id)
        except UserNotFoundById:
            error = UserNotFoundByIdException(user_id=user_id)
            logger.error(error.get_detail())
            raise error
        return UserResponse.model_validate(obj=user)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserResponse:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_login(session=session, login=login)
        except UserNotFoundByUsername:
            error = UserNotFoundByUsernameException(username=login)
            logger.error(error.get_detail())
            raise error
        return UserResponse.model_validate(obj=user)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequest) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_login(session=session, login=data.username)
            except UserAlreadyExist:
                error = UserAlreadyExistExeption(username=data.username)
                logger.error(error.get_detail())
                raise error
            except UserNotFoundByUsername:
                pass
            if data.email:
                get_existing_email = await session.execute(
                    select(self._repo._model)
                    .where(self._repo._model.email == data.email)
                )
                existing_email = get_existing_email.scalar_one_or_none()
                if existing_email:
                    error = UserEmailIsNotUniqueException(user_email=data.email)
                    logger.error(error.get_detail())
                    raise error

        user = await self._repo.create_user(
            session=session,
            data = data,
        )
        await session.commit()
        await session.refresh(user)
        logger.info(
                f"Зарегистрирован новый пользователь: {user.username}",
                extra={
                    "user_id": user.id,
                    "username": user.username,
                    "event": "user_created"
                }
            )
        return UserResponse.model_validate(obj=user)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, user_id: int, current_user_id: int, data: UserUpdate
    ) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_id(session=session, user_id=user_id)
                if current_user_id != user_id:
                    error = UserPermisionException(current_user_id=current_user_id)
                    logger.error(error.get_detail())
                    raise error
            except UserDoesNotExist:
                error = UserNotFoundByIdException(user_id=user_id)
                logger.error(error.get_detail())
                raise error
            if data.email and data.email != user.email:
                get_existing_email = await session.execute(
                    select(self._repo._model)
                    .where(self._repo._model.email == data.email)
                )
                existing_email = get_existing_email.scalar_one_or_none()
                if existing_email:
                    error = UserEmailIsNotUniqueException(user_email=data.email)
                    logger.error(error.get_detail())
                    raise error
            user = await self._repo.update_user(session=session, user=user, data=data)
            await session.commit()
            await session.refresh(user)
            logger.info(
                    f"Данные пользователя {user.username} обновлены",
                    extra={
                        "event": "user_updated"
                    }
                )
            return UserResponse.model_validate(obj=user)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user_id: int) -> None:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_id(session=session, user_id=user_id)
                if current_user_id != user_id:
                    raise UserPermissionDenied
            except UserNotFoundById:
                error = UserNotFoundByIdException(user_id=user_id)
                logger.error(error.get_detail())
                raise error
            
            except UserPermissionDenied:
                error = UserPermisionException(current_user_id=current_user_id)
                logger.error(error.get_detail())
                raise error
            logger.info(
                f"Пользователь {user.username} удален",
                extra={
                    "event": "user_deleted"
                }
            )
            await self._repo.delete_user(session=session, user=user)
            await session.commit()
