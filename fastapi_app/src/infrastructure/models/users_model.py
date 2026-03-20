from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from posts_model import Post


class User(Base):
    __tablename__ = "blog_users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    username: Mapped[str] = mapped_column(String(128), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self):
        return self.username
