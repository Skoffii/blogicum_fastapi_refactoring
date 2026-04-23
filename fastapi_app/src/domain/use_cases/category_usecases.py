from infrastructure.database import database
from infrastructure.repos.category_rep import CategoryRepository
from schemas.category import CategoryResponse
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
        title: str, 
        slug: str, 
        description: str, 
        is_published: bool = True
    ) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.create_category(
                    session=session,
                    title=title,
                    slug=slug,
                    description=description,
                    is_published=is_published
                )
                session.commit()
            except CategoryAlreadyExist:
                raise CategoryAlreadyExistException(category_slug=slug)
        
        return CategoryResponse.model_validate(category)


async def execute(
        self,
        category_id: int,
        title: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_published: bool | None = None
    ) -> CategoryResponse:
        with self._database.session() as session:
            try:
                # 1. Находим категорию
                category = self._repo.get_by_id(session=session, category_id=category_id)
                
                # 2. Обновляем данные
                updated_category = self._repo.update_category(
                    session=session,
                    category=category,
                    title=title,
                    slug=slug,
                    description=description,
                    is_published=is_published
                )
                
                # 3. Сохраняем изменения
                session.commit()
                
            except CategoryNotFoundById:
                raise CategoryNotFoundByIdException(category_id=category_id)
            except CategoryAlreadyExist:
                raise CategoryAlreadyExistException(slug=slug)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_id(session=session, category_id=category_id)
                self._repo.delete_category(session=session, category=category)
                session.commit()
            except CategoryNotFoundById:
                raise CategoryNotFoundByIdException(category_id=category_id)