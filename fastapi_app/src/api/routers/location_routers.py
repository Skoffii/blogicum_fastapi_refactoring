from fastapi import APIRouter, status, Depends

from schemas.location import LocationResponse
from domain.use_cases.location_usecases import *
from api.depends import get_location_by_id

router = APIRouter()


@router.get(
    "/location/{location_id}",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponse,
)
async def get_location(
    location_id: int, use_case: GetLocationByIdUseCase = Depends(get_location_by_id)
) -> LocationResponse:
    location = await use_case.execute(location_id=location_id)
    return location
