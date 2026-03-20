from typing import Type, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.posts_model import Post
from schemas.posts import PostRequest, PostUpdate


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_posts(self, session: Session, skip: int = 0, limit: int = 20) -> List[Post]:
        now = datetime.now()
        query = (
            session.query(self._model)
            .join(self._model.category)
            .where(
                self._model.is_published,
                self._model.pub_date <= now,
                self._model.category.is_published,
            )
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        query = session.query(self._model).where(self._model.id == post_id)
        return query.scalar()

    def get_by_author(
        self, session: Session, author_id: int, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    def get_by_category(
        self, session: Session, category_id: int, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.category_id == category_id)
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    def create_post(self, session: Session, data: PostRequest, author_id: int) -> Post:
        new_post = self._model(
            data.model_dump(), author_id=author_id, pub_date=datetime.now()
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

    def update_post(self, session: Session, post: Post, data: PostUpdate) -> Post:
        up_post = data.model_dump(exclude_unset=True)
        for key, value in up_post.items():
            setattr(post, key, value)

        session.commit()
        session.refresh(post)
        return post

    def delete_post(self, session: Session, post: Post) -> None:
        session.delete(post)
        session.commit()
