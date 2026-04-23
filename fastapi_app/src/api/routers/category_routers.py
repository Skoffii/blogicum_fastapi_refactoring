from fastapi import APIRouter, status, HTTPException, Depends

from schemas.category import CategoryResponse
from domain.use_cases.category_usecases import (
    GetCategoryBySlugUseCase,
    GetCategoryByIdUseCase,
)
from api.depends import (
    get_category_by_slug_use_case,
    get_category_by_id_use_case,
)
from core.exceptions.domain_exceptions import (
    CategoryNotFoundBySlugException,
    CategoryNotFoundByIdException,
)

router = APIRouter(prefix="/api/v1")


@router.get(
    "/categories/slug/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
)
async def get_category_by_slug(
    slug: str,
    use_case: GetCategoryBySlugUseCase = Depends(get_category_by_slug_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(slug=slug)
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.get(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )