import logging
from infrastructure.database import database
from infrastructure.repos.category_rep import CategoryRepository
from schemas.category import CategoryResponse, CategoryUpdate, CategoryRequest
from typing import List

from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *

logger = logging.getLogger(__name__)

class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[CategoryResponse]:
        async with self._database.session() as session:
            categories = await self._repo.get_all(session=session, skip=skip, limit=limit)
        return [CategoryResponse.model_validate(cat) for cat in categories]


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_slug(session=session, slug=slug)
            except CategoryNotFoundByName:
                error = CategoryNotFoundBySlugException(category_slug=slug)
                logger.error(error.get_detail())
                raise error
        return CategoryResponse.model_validate(obj=category)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_id(
                    session=session, category_id=category_id
                )
            except CategoryNotFoundById:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.get_detail())
                raise error
        return CategoryResponse.model_validate(obj=category)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        data: CategoryRequest,
    ) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.create_category(
                    session=session,
                    data=data,
                )
                session.commit()
            except CategoryAlreadyExist:
                error = CategoryAlreadyExistException(slug=data.slug)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(category)
            logger.info(
                    f"Категория {category.slug} создана",
                    extra={
                        "event": "category_created"
                    }
                )
            return CategoryResponse.model_validate(category)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        slug: str,
        data: CategoryUpdate,
    ) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_slug(session=session, slug=slug)
                updated_category = self._repo.update_category(
                    session=session,
                    data = data
                )
            except CategoryNotFoundByName:
                error = CategoryNotFoundBySlugException(category_slug=slug)
                logger.error(error.get_detail())
                raise error
            except CategoryAlreadyExist:
                error = CategoryAlreadyExistException(slug=data.slug)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(category)
            logger.info(
                f"Категория {category.slug} обновлена",
                extra={
                    "event": "category_updated"
                }
            )
            return CategoryResponse.model_validate(updated_category)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_id(
                    session=session, category_id=category_id
                )
                self._repo.delete_category(session=session, category=category)
                logger.info(
                    f"Категория {category.slug} удалена",
                    extra={
                        "event": "category_deleted"
                    }
                )
            except CategoryNotFoundById:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.get_detail())
                raise error
            session.commit()
