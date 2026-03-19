from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'blog_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128))

    posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return self.username
