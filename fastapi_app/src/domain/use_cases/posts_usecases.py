from typing import List, Optional
from fastapi import status, HTTPException
from datetime import datetime

from infrastructure.database import database
from infrastructure.repos.post_rep import PostRepository
from infrastructure.repos.user_rep import UserRepository
from infrastructure.repos.category_rep import CategoryRepository
from src.schemas.posts import PostRequest, PostResponse, PostUpdate
from src.schemas.users import UserResponse


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
            self, skip: int = 0, limit: int = 20
            ) -> List[PostResponse]:
        with self._database.session() as session:
            posts = self._repo.get_posts(
                session=session,
                skip=skip,
                limit=limit
                )
        return [PostResponse.model_validate(obj=post) for post in posts]


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, cur_user_id: Optional[int] = None
    ) -> PostResponse:
        with self._database.session() as session:
            post = self._repo.get_by_id(session=session, post_id=post_id)

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            can_view = False
            if cur_user_id == post.author_id:
                can_view = True
            elif (
                post.is_published
                and post.category.is_published
                and post.pub_date <= datetime.now()
            ):
                can_view = True

            if not can_view:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return PostResponse.model_validate(obj=post)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(
            self, login: str, skip: int = 0, limit: int = 10
            ) -> dict:
        with self._database.session() as session:
            user = self._user_repo.get_by_login(session=session, login=login)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            posts = self._repo.get_by_author(
                session=session, author_id=user.id, skip=skip, limit=limit
            )

        return {
            "user": UserResponse.model_validate(obj=user),
            "posts": [PostResponse.model_validate(obj=post) for post in posts],
        }


class GetPostsByCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()

    async def execute(
        self, category_slug: str, skip: int = 0, limit: int = 10
    ) -> List[PostResponse]:
        with self._database.session() as session:
            category = self._category_repo.get_by_slug(
                session=session,
                slug=category_slug
            )

            if not category or not category.is_published:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            posts = self._repo.get_by_category(
                session=session,
                category_id=category.id,
                skip=skip,
                limit=limit
            )

        return [PostResponse.model_validate(obj=post) for post in posts]


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequest, author_id: int) -> PostRequest:
        with self._database.session() as session:
            post = self._repo.create(
                session=session,
                data=data,
                author_id=author_id
                )

        return PostResponse.model_validate(obj=post)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, data: PostUpdate, current_user_id: int
    ) -> PostResponse:
        with self._database.session() as session:
            post = self._repo.get_by_id(session=session, post_id=post_id)

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if current_user_id != post.author_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

            post = self._repo.update(session=session, post=post, data=data)

        return PostResponse.model_validate(obj=post)
