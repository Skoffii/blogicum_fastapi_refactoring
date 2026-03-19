from sqlalchemy import Column, Boolean, String, Text, Integer
import re

from database import Base


class Category(Base):
    __tablename__ = 'blog_category'

    id = Column(Integer, primary_key=True)
    is_published = Column(Boolean, default=True)
    title = Column(String(256))
    description = Column(Text)
    slug = Column(String(200), unique=True, index=True)

    @staticmethod
    def validate_slug(slug):
        if not re.match(r"^[-a-zA-Z0-9_]+$", slug):
            raise ValueError("Invalid slug format")
        return slug

    def __repr__(self):
        return self.title
