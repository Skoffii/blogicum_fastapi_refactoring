from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.location import LocationResponse, LocationRequest, LocationUpdate
from schemas.error import ErrorResponse, ValidationErrorResponse
from domain.use_cases.location_usecases import (
    GetLocationByIdUseCase,
    GetAllLocationsUseCase,
    CreateLocationUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase,
)
from api.depends import (
    get_location_by_id,
    get_all_locations_use_case,
    create_location_use_case,
    update_location_use_case,
    delete_location_use_case,
)
from core.exceptions.domain_exceptions import (
    LocationAlreadyExistException,
    LocationNotFoundByIdException,
)

router = APIRouter()


@router.get(
    "/locations/{location_id}",
    response_model=LocationResponse,
    responses={
        200: {"model": LocationResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(get_location_by_id),
) -> LocationResponse:
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.get(
    "/locations/",
    response_model=List[LocationResponse],
    responses={
        200: {"model": LocationResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_all_locations(
    skip: int = 0,
    limit: int = 20,
    use_case: GetAllLocationsUseCase = Depends(get_all_locations_use_case),
) -> List[LocationResponse]:
    try:
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.post(
    "/locations/{location_id}",
    response_model=LocationResponse,
    responses={
        200: {"model": LocationResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_location(
    data: LocationRequest,
    use_case: CreateLocationUseCase = Depends(create_location_use_case),
) -> LocationResponse:
    try:
        return await use_case.execute(data=data)
    except LocationAlreadyExistException as exc:
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
    "/locations/{location_id}",
    response_model=LocationResponse,
    responses={
        200: {"model": LocationResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_location(
    location_id: int,
    data: LocationUpdate,
    use_case: UpdateLocationUseCase = Depends(update_location_use_case),
) -> LocationResponse:
    try:
        return await use_case.execute(data=data, location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except LocationAlreadyExistException as exc:
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
    "/locations/{location_id}",
    responses={
        204: {"detail": "NO_CONTENT"},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_location(
    location_id: int,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
) -> None:
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
