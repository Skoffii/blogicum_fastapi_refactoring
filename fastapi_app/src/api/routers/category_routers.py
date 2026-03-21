from fastapi import APIRouter, status, Depends

from schemas.category import CategoryResponse
from domain.use_cases.category_usecases import *
from api.depends import get_category_by_id_use_case, get_category_by_slug_use_case

router = APIRouter()


@router.get(
    "/category/{category_slug}/",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
)
async def category_by_slug(
    category_slug: str,
    use_case: GetCategoryBySlugUseCase = Depends(get_category_by_slug_use_case),
) -> CategoryResponse:
    category = await use_case.execute(category_slug=category_slug)
    return category


@router.get(
    "/category/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
)
async def category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case),
) -> CategoryResponse:
    category = await use_case.execute(category_id=category_id)
    return category
