from infrastructure.database import database
from infrastructure.repos.category_rep import CategoryRepository
from src.schemas.category import CategoryResponse
from fastapi import HTTPException, status


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponse:
        with self._database.session() as session:
            category = self._repo.get_by_slug(session=session, slug=slug)

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND
                )

        return CategoryResponse.model_validate(obj=category)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponse:
        with self._database.session() as session:
            category = self._repo.get_by_id(
                session=session, category_id=category_id
                )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND
                )

        return CategoryResponse.model_validate(obj=category)
