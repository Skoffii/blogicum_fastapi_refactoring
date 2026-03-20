from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
        )
    name: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return self.name
