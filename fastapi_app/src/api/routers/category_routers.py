from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.category import CategoryRequest, CategoryResponse, CategoryUpdate
from domain.use_cases.category_usecases import (
    GetAllCategoriesUseCase,
    GetCategoryBySlugUseCase,
    GetCategoryByIdUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from schemas.error import ErrorResponse, ValidationErrorResponse

from api.depends import (
    get_category_by_slug_use_case,
    get_category_by_id_use_case,
    get_all_categories_use_case,
    create_category_use_case,
    update_category_use_case,
    delete_category_use_case,
)
from core.exceptions.domain_exceptions import (
    CategoryNotFoundBySlugException,
    CategoryNotFoundByIdException,
    CategoryAlreadyExistException,
)

router = APIRouter()


@router.get(
    "/categories/",
    response_model=List[CategoryResponse],
    responses={
        200: {"model": CategoryResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_all_categories(
    skip: int = 0,
    limit: int = 20,
    use_case: GetAllCategoriesUseCase = Depends(get_all_categories_use_case),
) -> List[CategoryResponse]:
    try:
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/categories/{slug}",
    response_model=CategoryResponse,
    responses={
        200: {"model": CategoryResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
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
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/categories/id/{category_id}",
    response_model=CategoryResponse,
    responses={
        200: {"model": CategoryResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
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
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.post(
    "/categories/{slug}",
    response_model=CategoryResponse,
    responses={
        200: {"model": CategoryResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_category(
    category: CategoryRequest,
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(data=category)
    except CategoryAlreadyExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.put(
    "/categories/{slug}",
    response_model=CategoryResponse,
    responses={
        201: {"model": CategoryResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_category(
    slug: str,
    category: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends(update_category_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(
            slug=slug,
            data=category,
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except CategoryAlreadyExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.delete(
    "/categories/{slug}/delete",
    responses={
        204: {"detail": "NO_CONTENT"},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
) -> None:
    try:
        await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
