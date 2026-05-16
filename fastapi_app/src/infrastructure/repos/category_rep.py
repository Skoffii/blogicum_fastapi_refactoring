from typing import Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.models.categories_model import Category
from core.exceptions.infrastructure_exceptions import *
from schemas.category import CategoryRequest, CategoryUpdate


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Category]:
        query = await session.execute(select(self._model).offset(skip).limit(limit))
        return query.scalars().all()

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Optional[Category]:
        query = await session.execute(select(self._model).where(self._model.slug == slug))
        category = query.scalar()
        if not category:
            raise CategoryNotFoundByName
        return category

    async def get_by_id(self, session: AsyncSession, category_id: int) -> Optional[Category]:
        query = await session.execute(select(self._model).where(self._model.id == category_id))
        category = query.scalar()
        if not category:
            raise CategoryNotFoundById
        return category

    async def create_category(
        self,
        session: AsyncSession,
        data: CategoryRequest
    ) -> Category:
        if_existing = await session.execute(select(self._model).where(self._model.slug == data.slug))
        existing = if_existing.scalar()
        if existing:
            raise CategoryAlreadyExist
        new_category = self._model(
            title=data.title,
            slug=data.slug,
            description=data.description,
            is_published=data.is_published,
        )
        session.add(new_category)
        await session.flush()
        await session.refresh(new_category)
        return new_category

    async def update_category(
        self,
        session: AsyncSession,
        category: Category,
        data: CategoryUpdate
    ) -> Category:
        if data.slug and data.slug != category.slug:
            if_existing = await session.execute(
                select(self._model).where(self._model.slug == data.slug)
            )
            existing = if_existing.scalar()
            if existing:
                raise CategoryAlreadyExist
            category.slug = data.slug

        if data.title:
            category.title = data.title
        if data.description:
            category.description = data.description
        if data.is_published is not None:
            category.is_published = data.is_published
        return category

    async def delete_category(self, session: AsyncSession, category: Category) -> None:
        exist = await self.get_by_id(session, category.id)
        if not exist:
            raise CategoryNotFoundById
        await session.delete(category)
