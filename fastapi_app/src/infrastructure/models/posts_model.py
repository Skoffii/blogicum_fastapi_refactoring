from sqlalchemy import Boolean, DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime

from users_model import User
from locations_model import Location
from categories_model import Category
from comments_model import Comment

from database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False, name="Текст")
    pub_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    category_id: Mapped = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    author_id: Mapped["User"] = relationship(back_populates="posts")
    location: Mapped["Location"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def __repr__(self):
        return self.title
