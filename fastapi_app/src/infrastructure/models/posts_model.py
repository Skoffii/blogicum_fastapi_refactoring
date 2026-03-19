from sqlalchemy import (
    Column, Boolean, DateTime, String, Text, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
import datetime

from database import Base


class Post(Base):
    __tablename__ = "blog_post"

    post_id = Column(Integer, primary_key=True)
    is_published = Column(Boolean, default=True, name="Опубликовано")
    created_at = Column(DateTime, default=datetime.now(), name="Добавлено")
    title = Column(String(256), name="Заголовок")
    text = Column(Text, name="Текст")
    pub_date = Column(DateTime)
    image = Column(String, nullable=True)

    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                       nullable=False)
    location_id = Column(
        Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    location = relationship("Location")
    category = relationship("Category")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return self.title
