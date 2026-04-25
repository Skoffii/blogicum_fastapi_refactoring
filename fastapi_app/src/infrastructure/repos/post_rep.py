from typing import Type, List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from infrastructure.models.posts_model import Post
from infrastructure.models.categories_model import Category
from infrastructure.models.locations_model import Location
from infrastructure.models.users_model import User
from schemas.posts import PostRequest, PostUpdate
from core.exceptions.infrastructure_exceptions import *


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_posts(self, session: Session, skip: int = 0, limit: int = 20) -> List[Post]:
        now = datetime.now()

        query = (
            session.query(self._model)
            .outerjoin(self._model.category)
            .where(
                self._model.is_published,
                self._model.pub_date <= now,
                (self._model.category_slug.is_(None) | Category.is_published),
            )
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        query = (
            session.query(self._model)
            .options(joinedload(self._model.category))
            .where(self._model.id == post_id)
        )
        post = query.scalar()
        if not post:
            raise PostNotFoundById
        return post

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
        author = session.query(User).where(User.id == author_id).scalar()
        if not author:
            raise UserDoesNotExist
        return query.all()

    def get_by_category(
        self, session: Session, category_slug: str, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.category_slug == category_slug)
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        category = session.query(Category).where(Category.slug == category_slug).scalar()
        if not category:
            raise CategoryNotFoundById
        return query.all()

    def create_post(self, session: Session, data: PostRequest, author_id: int) -> Post:
        try:
            author = session.query(User).where(User.id == author_id).scalar()
            if not author:
                raise UserNotFoundById
            if data.category_slug:
                category = session.query(Category).where(Category.slug == data.category_slug).scalar()
                if not category:
                    raise CategoryNotFoundByName
                if not category.is_published:
                    raise CategoryNotPublished

            if data.location_id:
                location = session.query(Location).where(Location.id == data.location_id).scalar()
                if not location:
                    raise LocationNotFoundById
                
        
            new_post = self._model(
                **data.model_dump(),
                author_id=author_id,
                created_at=datetime.now(),
            )
            session.add(new_post)
            session.flush()
            session.refresh(new_post)
            return new_post
        
        except IntegrityError as e:
            session.rollback()
            raise DatabaseIntegrityError(
                original_error=e
            )

    def update_post(self, session: Session, post: Post, data: PostUpdate) -> Post:
        up_post = data.model_dump(exclude_unset=True)
        for key, value in up_post.items():
            setattr(post, key, value)
        exist = self.get_by_id(session, post.id)
        if not exist:
            raise PostDoesNotExist
        if data.location_id:
            location = session.query(Location).where(Location.id == data.location_id).scalar()
            if not location:
                raise LocationNotFoundById
        if data.category_slug:
            category = session.query(Category).where(Category.slug == data.category_slug).scalar()
            if not category:
                raise CategoryNotFoundByName
        return post

    def delete_post(self, session: Session, post: Post) -> None:
        exist = self.get_by_id(session, post.id)
        if not exist:
            raise PostDoesNotExist
        session.delete(post)

    def update_post_image(self, session: Session, post_id: int, image_filename: str) -> Post:
        post = self.get_by_id(session=session, post_id=post_id)
        post.image = image_filename
        session.flush()
        return post
