from sqlalchemy import Column, DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from database import Base


class Comment(Base):
    __tablename__ = 'blog_comment'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.now())

    post_id = Column(Integer, ForeignKey('blog_post.id', ondelete='CASCADE'))
    author = Column(String, ForeignKey('users_model.id'))

    post = relationship('Post', back_populates="comments")
    author = relationship('User')

    def __repr__(self):
        return self.text
