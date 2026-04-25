from infrastructure.database import database
from infrastructure.repos.category_rep import CategoryRepository
from schemas.category import CategoryResponse, CategoryUpdate, CategoryRequest
from typing import List

from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[CategoryResponse]:
        with self._database.session() as session:
            categories = self._repo.get_all(session=session, skip=skip, limit=limit)
        return [CategoryResponse.model_validate(cat) for cat in categories]


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_slug(session=session, slug=slug)
            except CategoryNotFoundByName:
                raise CategoryNotFoundBySlugException(category_slug=slug)
        return CategoryResponse.model_validate(obj=category)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_id(session=session, category_id=category_id)
            except CategoryNotFoundById:
                raise CategoryNotFoundByIdException(category_id=category_id)
        return CategoryResponse.model_validate(obj=category)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        data: CategoryRequest,
    ) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.create_category(
                    session=session,
                    title=data.title,
                    slug=data.slug,
                    description=data.description,
                    is_published=data.is_published
                )
                session.commit()
            except CategoryAlreadyExist:
                raise CategoryAlreadyExistException(slug=data.slug)
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
        with self._database.session() as session:
            try:
                category = self._repo.get_by_slug(session=session, slug=slug)
                updated_category = self._repo.update_category(
                    session=session,
                    category=category,
                    title=data.title,
                    slug=data.slug,
                    description=data.description,
                    is_published=data.is_published
                )
            except CategoryNotFoundByName:
                raise CategoryNotFoundBySlugException(category_slug=slug)
            except CategoryAlreadyExist:
                raise CategoryAlreadyExistException(slug=data.slug)
            session.commit()
        return CategoryResponse.model_validate(updated_category)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_id(session=session, category_id=category_id)
                self._repo.delete_category(session=session, category=category)
            except CategoryNotFoundById:
                raise CategoryNotFoundByIdException(category_id=category_id)