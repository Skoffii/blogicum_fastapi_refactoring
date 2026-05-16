from infrastructure.database import database
from infrastructure.repos.location_rep import LocationRepository
from schemas.location import LocationResponse, LocationUpdate, LocationRequest
from typing import List
import logging
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


logger = logging.getLogger(__name__)

class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponse:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_by_id(
                    session=session, location_id=location_id
                )
            except LocationNotFoundById:
                error = LocationNotFoundByIdException(location_id=location_id)
                logger.error(error.get_detail())
                raise error
        return LocationResponse.model_validate(obj=location)


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[LocationResponse]:
        async with self._database.session() as session:
            locations = await self._repo.get_all(session=session, skip=skip, limit=limit)
        return [LocationResponse.model_validate(loc) for loc in locations]


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationRequest) -> LocationResponse:
        async with self._database.session() as session:
            try:
                location = await self._repo.create_location(session=session, data=data)
                session.commit()
            except LocationAlreadyExist:
                error = LocationAlreadyExistException(location_name=data.name)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(location)
            logger.info(
                    f"Локация {location.name} создана",
                    extra={
                        "event": "location_created"
                    }
                )
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
        async with self._database.session() as session:
            try:
                location = await self._repo.get_by_id(
                    session=session, location_id=location_id
                )
                updated_location = self._repo.update_location(
                    session=session,
                    location=location,
                    name=data.name,
                    is_published=data.is_published,
                )
            except LocationNotFoundById:
                error = LocationNotFoundByIdException(location_id=location.location_id)
                logger.error(error.get_detail())
                raise error
            except LocationAlreadyExist:
                error = LocationAlreadyExistException(
                    location_name=updated_location.name
                )
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(location)
            logger.info(
                f"Локация {location.name} обновлена",
                extra={
                    "event": "location_updated"
                }
            )
            return LocationResponse.model_validate(updated_location)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_by_id(
                    session=session, location_id=location_id
                )
                await self._repo.delete_location(session=session, location=location)
                logger.info(
                    f"Локация {location.name} удалена",
                    extra={
                        "event": "location_deleted"
                    }
                )
            except LocationNotFoundById:
                error = LocationNotFoundByIdException(location_id=location_id)
                logger.error(error.get_detail())
                raise error
            await session.commit()
