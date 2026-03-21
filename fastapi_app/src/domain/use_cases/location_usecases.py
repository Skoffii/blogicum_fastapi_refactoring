from infrastructure.database import database
from infrastructure.repos.location_rep import LocationRepository
from schemas.location import LocationResponse
from fastapi import HTTPException, status


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponse:
        with self._database.session() as session:
            location = self._repo.get_by_id(session=session, location_id=location_id)

            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
                )

        return LocationResponse.model_validate(obj=location)
