from fastapi import APIRouter, status, HTTPException, Depends

from schemas.location import LocationResponse
from domain.use_cases.location_usecases import (
    GetLocationByIdUseCase,
)
from api.depends import (
    get_location_by_id
)
from core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
)

router = APIRouter(prefix="/api/v1")


@router.get(
    "/locations/{location_id}",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponse,
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
            detail=exc.detail,
        )