from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, Optional
from schemas.users import UserRequest
from sqlalchemy import select
from infrastructure.models.users_model import User
from schemas.users import UserUpdate
from datetime import datetime
from resourses.auth import get_password_hash
from core.exceptions.infrastructure_exceptions import (
    UserNotFoundById,
    UserNotFoundByUsername,
    UserAlreadyExist,
    UserDoesNotExist,
    UserEmailAlreadyExist,
)


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        query = await session.execute(select(self._model).where(self._model.id == user_id))
        user = query.scalar()
        if not user:
            raise UserNotFoundById
        return user

    async def get_by_login(self, session: AsyncSession, login: str) -> Optional[User]:
        query = await session.execute(select(self._model).where(self._model.username == login))
        user = query.scalar()
        if not user:
            raise UserNotFoundByUsername
        return user

    async def create_user(
        self,
        session: AsyncSession,
        data: UserRequest,
    ) -> User:
        try:
            exist = await self.get_by_login(session, data.username)
            if exist:
                raise UserAlreadyExist
        except UserNotFoundByUsername:
            pass
        hashed_password = get_password_hash(data.password.get_secret_value())
        if data.email:
            if_exist_email = await session.execute(
                select(self._model).where(self._model.email == data.email)
            )
            exist_email = if_exist_email.scalar()
            if exist_email:
                raise UserEmailAlreadyExist
        new_user = self._model(
            username=data.username,
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            date_joined=datetime.now(),
        )
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        return new_user

    async def update_user(self, session: AsyncSession, user: User, data: UserUpdate) -> User:
        update_user = data.model_dump(exclude_unset=True)
        exist = await self.get_by_id(session, user.id)
        if not exist:
            raise UserDoesNotExist
        if data.email:
            get_exist_email = await session.execute(
                select(self._model)
                .where(self._model.email == data.email)
            )
            exist_email = get_exist_email.scalar()
            if exist_email:
                raise UserEmailAlreadyExist
        for key, value in update_user.items():
            setattr(user, key, value)
        return user

    async def delete_user(self, session: AsyncSession, user: User) -> None:
        exist = await self.get_by_id(session, user.id)
        if not exist:
            raise UserDoesNotExist
        await session.delete(user)
