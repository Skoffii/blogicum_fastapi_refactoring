from typing import Optional
from sqlalchemy.orm import Session

from models.locations_model import Location


class LocationRepository:
    def __init__(self):
        self._model[Location] = Location

    def get_by_id(
            self, session: Session, location_id: int
            ) -> Optional[Location]:
        query = session.query(self._model).where(self._model.id == location_id)
        return query.scalar()
