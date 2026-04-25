from sqlalchemy import DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from infrastructure.database import Base
from .posts_model import Post
from .users_model import User


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[str] = mapped_column(
        String, ForeignKey("auth_user.id"), nullable=False
    )
    image: Mapped[str] = mapped_column(String, nullable=True)

    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")

    def __repr__(self):
        return self.text
