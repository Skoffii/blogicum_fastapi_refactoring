from sqlalchemy.orm import Session
from typing import Type, Optional
from infrastructure.models.users_model import User
from schemas.users import UserUpdate
from datetime import datetime


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        query = session.query(self._model).where(self._model.id == user_id)
        return query.scalar()

    def get_by_login(self, session: Session, login: int) -> Optional[User]:
        query = session.query(self._model).where(self._model.username == login)
        return query.scalar()

    def create_user(
        self,
        session: Session,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True,
        last_login: Optional[datetime] = None,
        date_joined: Optional[datetime] = None,
    ) -> User:

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
        session.commit()
        session.refresh(new_user)
        return new_user

    def update_user(self, session: Session, user: User, data: UserUpdate) -> User:
        update_user = data.model_dump(exclude_unset=True)
        for key, value in update_user.items():
            setattr(user, key, value)
        session.commit
        session.refresh(user)
        return user

    def delete_user(self, session: Session, user: User) -> None:
        session.delete(user)
        session.commit()
