from typing import Optional, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.models.locations_model import Location
from core.exceptions.infrastructure_exceptions import *
from schemas.location import LocationRequest, LocationUpdate


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    async def get_by_id(self, session: AsyncSession, location_id: int) -> Optional[Location]:
        query = await session.execute(select(self._model).where(self._model.id == location_id))
        location = query.scalar()
        if not location:
            raise LocationNotFoundById
        return location

    async def get_by_name(self, session: AsyncSession, location_name: str) -> Optional[Location]:
        query = await session.execute(select(self._model).where(self._model.name == location_name))
        location = query.scalar()
        if not location:
            raise LocationNotFoundByName
        return location

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Location]:
        query = await session.execute(select(self._model).offset(skip).limit(limit))
        return query.scalars().all()

    async def create_location(self, session: AsyncSession, data: LocationRequest) -> Location:
        if_existing = await session.execute(
            select(self._model).where(self._model.name == data.name)
        )
        existing = if_existing.scalar()
        if existing:
            raise LocationAlreadyExist
        new_location = self._model(name=data.name, is_published=data.is_published)
        session.add(new_location)
        await session.flush()
        await session.refresh(new_location)
        return new_location

    async def update_location(
        self,
        session: AsyncSession,
        location: Location,
        data: LocationUpdate
    ) -> Location:
        if data.name and data.name != location.name:
            if_existing = await session.execute(
                select(self._model).where(self._model.name == data.name)
            )
            existing = if_existing.scalar()
            if existing:
                raise LocationAlreadyExist
            location.name = data.name
        if data.is_published is not None:
            location.is_published = data.is_published
        return location

    async def delete_location(self, session: AsyncSession, location: Location) -> None:
        exist = await self.get_by_id(session, location.id)
        if not exist:
            raise LocationNotFoundById
        await session.delete(location)
