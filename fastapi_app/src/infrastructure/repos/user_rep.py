from sqlalchemy.orm import Session
from typing import Type, Optional
from models.users_model import User
from schemas.users import UserRequest, UserUpdate


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        query = session.query(self._model).where(self._model.id == user_id)
        return query.scalar()

    def get_by_login(self, session: Session, login: int) -> Optional[User]:
        query = session.query(self._model).where(self._model.login == login)
        return query.scalar()

    def create_user(self, session: Session, data: UserRequest) -> User:
        new_user = self._model(**data.model_dump())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    def update_user(
            self, session: Session, user: User, data: UserUpdate
            ) -> User:
        update_user = data.model_dump(exclude_unset=True)
        for key, value in update_user.items():
            setattr(user, key, value)
        session.commit
        session.refresh(user)
        return user

    def delete_user(self, session: Session, user: User) -> None:
        session.delete(user)
        session.commit()
