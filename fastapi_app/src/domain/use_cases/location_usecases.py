from infrastructure.database import database
from infrastructure.repos.location_rep import LocationRepository
from schemas.location import LocationResponse, LocationUpdate, LocationRequest

from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponse:
        with self._database.session() as session:
            try:
                location = self._repo.get_by_id(session=session, location_id=location_id)
            except LocationNotFoundById:
                raise LocationNotFoundByIdException(location_id=location_id)
        return LocationResponse.model_validate(obj=location)
    


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[LocationResponse]:
        with self._database.session() as session:
            locations = self._repo.get_all(session=session, skip=skip, limit=limit)
        return [LocationResponse.model_validate(loc) for loc in locations]


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationRequest) -> LocationResponse:
        with self._database.session() as session:
            try:
                location = self._repo.create_location(
                    session=session,
                    data=data)
                session.commit()
            except LocationAlreadyExist:
                raise LocationAlreadyExistException(location_name=data.name)
        return LocationResponse.model_validate(location)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        location_id: int,
        data: LocationUpdate,
    ) -> LocationUpdate:
        with self._database.session() as session:
            try:
                location = self._repo.get_by_id(session=session, location_id=location_id)
                updated_location = self._repo.update_location(
                    session=session,
                    location=location,
                    name=data.name,
                    is_published=data.is_published
                )
            except LocationNotFoundById:
                raise LocationNotFoundByIdException(location_id=location.location_id)
            except LocationAlreadyExist:
                raise LocationAlreadyExistException(location_name=updated_location.location_name)
        return LocationResponse.model_validate(updated_location)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            try:
                location = self._repo.get_by_id(session=session, location_id=location_id)
                self._repo.delete_location(session=session, location=location)
            except LocationNotFoundById:
                raise LocationNotFoundByIdException(location_id=location_id)