from typing import Type, Optional, List
from sqlalchemy.orm import Session

from infrastructure.models.categories_model import Category
from core.exceptions.infrastructure_exceptions import *


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_all(self, session: Session, skip: int = 0, limit: int = 20) -> List[Category]:
        query = session.query(self._model).offset(skip).limit(limit)
        return query.all()

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        query = session.query(self._model).where(self._model.slug == slug)
        category = query.scalar()
        if not category:
            raise CategoryNotFoundByName
        return category

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        query = session.query(self._model).where(self._model.id == category_id)
        category = query.scalar()
        if not category:
            raise CategoryNotFoundById
        return category

    def create_category(self, session: Session, title: str, slug: str, description: str, is_published: bool = True) -> Category:
        existing = session.query(self._model).where(self._model.slug == slug).scalar()
        if existing:
            raise CategoryAlreadyExist
        new_category = self._model(
            title=title,
            slug=slug,
            description=description,
            is_published=is_published,
        )
        session.add(new_category)
        session.flush()
        session.refresh(new_category)
        return new_category

    def update_category(self, session: Session, category: Category, title: str | None = None, slug: str | None = None, description: str | None = None, is_published: bool | None = None) -> Category:
        if slug and slug != category.slug:
            existing = session.query(self._model).where(self._model.slug == slug).scalar()
            if existing:
                raise CategoryAlreadyExist
            category.slug = slug

        if title:
            category.title = title
        if description:
            category.description = description
        if is_published is not None:
            category.is_published = is_published
        return category

    def delete_category(self, session: Session, category: Category) -> None:
        exist = self.get_by_id(session, category.id)
        if not exist:
            raise CategoryNotFoundById
        session.delete(category)
