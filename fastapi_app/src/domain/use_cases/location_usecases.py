from infrastructure.database import database
from infrastructure.repos.location_rep import LocationRepository
from schemas.location import LocationResponse

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
                raise LocationNotFoundByIdException
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

    async def execute(self, name: str, is_published: bool = True) -> LocationResponse:
        with self._database.session() as session:
            try:
                location = self._repo.create_location(session=session, name=name, is_published=is_published)
                session.commit()
            except LocationAlreadyExist:
                raise LocationAlreadyExistException(name=name)
        return LocationResponse.model_validate(location)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, 
        location_id: int, 
        location_name: str, 
        is_published: Optional[bool] = None
    ) -> LocationResponse:
        with self._database.session() as session:
            try:
                location = self._repo.get_by_id(session=session, location_id=location_id)
                updated_location = self._repo.update_location(
                    session=session, location=location, name=location_name, is_published=is_published
                )
            except LocationNotFoundById:
                raise LocationNotFoundByIdException(location_id=location_id)
            except LocationAlreadyExist:
                raise LocationAlreadyExistException(location_name=location_name)
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