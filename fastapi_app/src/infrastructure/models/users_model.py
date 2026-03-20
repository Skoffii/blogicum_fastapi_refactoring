from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from posts_model import Post


class User(Base):
    __tablename__ = "blog_users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    login: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
        )
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(256), nullable=True)
    email: Mapped[str] = mapped_column(String(256), nullable=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self):
        return self.username
