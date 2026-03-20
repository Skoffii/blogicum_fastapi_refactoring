from typing import Type, Optional
from sqlalchemy.orm import Session

from models.categories_model import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        query = session.query(self._model).where(self._model.slug == slug)
        return query.scalar()

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        query = session.query(self._model).where(self._model.id == category_id)
        return query.scalar()
