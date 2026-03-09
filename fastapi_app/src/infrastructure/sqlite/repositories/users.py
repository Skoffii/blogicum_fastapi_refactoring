from typing import Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.users import User


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, login: str) -> User:
        query = session.query(self._model).where(self._model.login == login)

        return query.scalar()
