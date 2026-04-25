from sqlalchemy.orm import Session
from typing import Type, Optional
from pydantic import SecretStr, EmailStr
from infrastructure.models.users_model import User
from schemas.users import UserUpdate
from datetime import datetime
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

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        query = session.query(self._model).where(self._model.id == user_id)
        user = query.scalar()
        if not user:
            raise UserNotFoundById
        return user

    def get_by_login(self, session: Session, login: str) -> Optional[User]:
        query = session.query(self._model).where(self._model.username == login)
        user = query.scalar()
        if not user:
            raise UserNotFoundByUsername
        return user

    def create_user(
        self,
        session: Session,
        username: str,
        password: SecretStr,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[EmailStr] = None,
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True,
        last_login: Optional[datetime] = None,
        date_joined: Optional[datetime] = None,
    ) -> User:
        try:
            exist = self.get_by_login(session, username)
            if exist:
                raise UserAlreadyExist
        except UserNotFoundByUsername:
            pass
        if email:
            exist_email = (
                session.query(self._model).where(self._model.email == email).scalar()
            )
            if exist_email:
                raise UserEmailAlreadyExist
        new_user = self._model(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            last_login=last_login,
            date_joined=date_joined or datetime.now(),
        )
        session.add(new_user)
        session.flush()
        session.refresh(new_user)
        return new_user

    def update_user(self, session: Session, user: User, data: UserUpdate) -> User:
        update_user = data.model_dump(exclude_unset=True)
        exist = self.get_by_id(session, user.id)
        if not exist:
            raise UserDoesNotExist
        if data.email:
            exist_email = (
                session.query(self._model)
                .where(self._model.email == data.email)
                .scalar()
            )
            if exist_email:
                raise UserEmailAlreadyExist
        for key, value in update_user.items():
            setattr(user, key, value)
        return user

    def delete_user(self, session: Session, user: User) -> None:
        exist = self.get_by_id(session, user.id)
        if not exist:
            raise UserDoesNotExist
        session.delete(user)
