from typing import Optional, Type, List
from sqlalchemy.orm import Session

from infrastructure.models.locations_model import Location
from core.exceptions.infrastructure_exceptions import *


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_by_id(self, session: Session, location_id: int) -> Optional[Location]:
        query = session.query(self._model).where(self._model.id == location_id)
        location = query.scalar()
        if not location:
            raise LocationNotFoundById
        return location

    def get_by_name(self, session: Session, location_name: int) -> Optional[Location]:
        query = session.query(self._model).where(self._model.name == location_name)
        location = query.scalar()
        if not location:
            raise LocationNotFoundByName
        return location

    def get_all(self, session: Session, skip: int = 0, limit: int = 20) -> List[Location]:
        query = session.query(self._model).offset(skip).limit(limit)
        return query.all()

    def create_location(self, session: Session, name: str, is_published: bool = True) -> Location:
        existing = session.query(self._model).where(self._model.name == name).scalar()
        if existing:
            raise LocationAlreadyExist
        new_location = self._model(name=name, is_published=is_published)
        session.add(new_location)
        session.flush()
        session.refresh(new_location)
        return new_location

    def update_location(self, session: Session, location: Location, name: str | None = None, is_published: bool | None = None) -> Location:
        if name and name != location.name:
            existing = session.query(self._model).where(self._model.name == name).scalar()
            if existing:
                raise LocationAlreadyExist
            location.name = name
        if is_published is not None:
            location.is_published = is_published
        return location

    def delete_location(self, session: Session, location: Location) -> None:
        exist = self.get_by_id(session, location.id)
        if not exist:
            raise LocationNotFoundById
        session.delete(location)
