from sqlalchemy import Column, Boolean, String, Integer

from database import Base


class Location(Base):
    __tablename__ = 'blog_location'

    location_id = Column(Integer, primary_key=True)
    is_published = Column(Boolean, default=True)
    name = Column(String(256))

    def __repr__(self):
        return self.name
