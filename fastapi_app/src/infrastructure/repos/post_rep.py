from typing import Type, List, Optional
from sqlalchemy.orm import joinedload
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.models.posts_model import Post
from infrastructure.models.categories_model import Category
from infrastructure.models.locations_model import Location
from infrastructure.models.users_model import User
from schemas.posts import PostRequest, PostUpdate
from core.exceptions.infrastructure_exceptions import *


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    async def get_posts(self, session: AsyncSession, skip: int = 0, limit: int = 20) -> List[Post]:
        now = datetime.now()

        query = (
            select(self._model)
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
        posts = await session.execute(query)
        return posts.scalars().all()

    async def get_by_id(self, session: AsyncSession, post_id: int) -> Optional[Post]:
        query = (
            select(self._model)
            .options(joinedload(self._model.category))
            .where(self._model.id == post_id)
        )
        result = await session.execute(query)
        post = result.scalar()
        if not post:
            raise PostNotFoundById
        return post

    async def get_by_author(
        self, session: AsyncSession, author_id: int, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        query = (
            select(self._model)
            .where(self._model.author_id == author_id)
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        get_author = select(User).where(User.id == author_id)
        author_result = await session.execute(get_author)
        author = author_result.scalar()
        if not author:
            raise UserDoesNotExist
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_category(
        self, session: AsyncSession, category_slug: str, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        query = (
            select(self._model)
            .where(self._model.category_slug == category_slug)
            .order_by(self._model.pub_date.desc())
            .offset(skip)
            .limit(limit)
        )
        get_category = select(Category).where(Category.slug == category_slug)
        category_res = await session.execute(get_category)
        category = category_res.scalar()
        if not category:
            raise CategoryNotFoundById
        result = await session.execute(query)
        return result.scalars().all()

    async def create_post(self, session: AsyncSession, data: PostRequest, author_id: int) -> Post:
        get_author = await session.execute(select(User).where(User.id == author_id))
        author = get_author.scalar()
        if not author:
            raise UserNotFoundById
        if data.category_slug:
            get_category = await session.execute(
                select(Category)
                .where(Category.slug == data.category_slug)
            )
            category = get_category.scalar()
            if not category:
                raise CategoryNotFoundByName
            if not category.is_published:
                raise CategoryNotPublished
        if data.location_id:
            get_location = await session.execute(
                select(Location)
                .where(Location.id == data.location_id)
            )
            location = get_location.scalar()
            if not location:
                raise LocationNotFoundById
        new_post = self._model(
            **data.model_dump(),
            author_id=author_id,
            created_at=datetime.now(),
            pub_date=datetime.now(),
        )
        session.add(new_post)
        await session.flush()
        await session.refresh(new_post)
        return new_post

    async def update_post(self, session: AsyncSession, post: Post, data: PostUpdate) -> Post:
        up_post = data.model_dump(exclude_unset=True)
        for key, value in up_post.items():
            setattr(post, key, value)
        exist = await self.get_by_id(session, post.id)
        if not exist:
            raise PostDoesNotExist
        if data.location_id:
            get_location = await session.execute(
                select(Location).where(Location.id == data.location_id)
            )
            location = get_location.scalar()
            if not location:
                raise LocationNotFoundById
        if data.category_slug:
            get_category = await session.execute(
                select(Category)
                .where(Category.slug == data.category_slug)
            )
            category = get_category.scalar()
            if not category:
                raise CategoryNotFoundByName
        return post

    async def delete_post(self, session: AsyncSession, post: Post) -> None:
        exist = await self.get_by_id(session, post.id)
        if not exist:
            raise PostDoesNotExist
        await session.delete(post)

    async def update_post_image(
        self, session: AsyncSession, post_id: int, image_filename: str
    ) -> Post:
        post = await self.get_by_id(session=session, post_id=post_id)
        post.image = image_filename
        await session.flush()
        return post
