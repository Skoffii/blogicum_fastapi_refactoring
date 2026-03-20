from sqlalchemy import Boolean, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
        )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
        )
    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False
        )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False
    )

    def __repr__(self):
        return self.title
