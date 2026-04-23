from typing import List, Optional
from fastapi import status, HTTPException
from datetime import datetime

from infrastructure.database import database
from infrastructure.repos.post_rep import PostRepository
from infrastructure.repos.user_rep import UserRepository
from infrastructure.repos.category_rep import CategoryRepository
from infrastructure.models.categories_model import Category
from schemas.posts import PostRequest, PostResponse, PostUpdate
from schemas.users import UserResponse
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[PostResponse]:
        with self._database.session() as session:
            posts = self._repo.get_posts(session=session, skip=skip, limit=limit)
        return [PostResponse.model_validate(obj=post) for post in posts]


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, cur_user_id: Optional[int] = None
    ) -> PostResponse:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session=session, post_id=post_id)

                can_view = False
                if cur_user_id == post.author_id:
                    can_view = True
                elif (
                    post.is_published
                    and (post.category is None or post.category.is_published)
                    and post.pub_date <= datetime.now()
                ):
                    can_view = True

                if not can_view:
                    raise PostAccessDenied
            except PostAccessDenied:
                raise UserPermissionDenied(cur_user_id=cur_user_id)
            except PostNotFoundById:
                raise PostNotFoundByIdException(post_id=post_id)
        return PostResponse.model_validate(obj=post)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, login: str, skip: int = 0, limit: int = 10) -> dict:
        with self._database.session() as session:
            user = self._user_repo.get_by_login(session=session, login=login)
            try:
                posts = self._repo.get_by_author(
                    session=session, author_id=user.id, skip=skip, limit=limit
                )
            except UserDoesNotExist:
                raise UserNotFoundByUsernameException(username=login)

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
            try:
                category = self._category_repo.get_by_slug(
                    session=session, slug=category_slug
                )
            except CategoryNotFoundByName:
                raise CategoryNotFoundBySlugException(category_slug=category_slug)
            posts = self._repo.get_by_category(
                session=session, category_id=category.id, skip=skip, limit=limit
            )
        return [PostResponse.model_validate(obj=post) for post in posts]


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequest, author_id: int) -> PostResponse:
        with self._database.session() as session:
            try:
                post = self._repo.create_post(
                    session=session, data=data, author_id=author_id
                )
            except UserNotFoundById:
                raise UserNotFoundByIdException(user_id=author_id)
            except CategoryNotFoundByName:
                raise CategoryNotFoundBySlugException(category_slug=data.category_name)
            except CategoryNotPublished:
                raise CategoryNotPublishedException(category_slug=data.category_name)

        return PostResponse.model_validate(obj=post)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, data: PostUpdate, current_user_id: int
    ) -> PostResponse:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session=session, post_id=post_id)

                if current_user_id != post.author_id:
                    raise PostAccessDenied
            except PostAccessDenied:
                raise UserPermisionException(current_user_id=current_user_id)
            except PostDoesNotExist:
                raise PostNotFoundByIdException(post_id=post_id)
            try:
                post = self._repo.update_post(session=session, post=post, data=data)
            except LocationNotFoundByName:
                raise LocationNotFoundByNameException(location_name=data.location_name)
            except CategoryNotFoundByName:
                raise CategoryNotFoundBySlugException(category_slug=data.category_name)

        return PostResponse.model_validate(obj=post)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session=session, post_id=post_id)

                if current_user_id != post.author_id:
                    raise PostAccessDenied
            except PostAccessDenied:
                raise UserPermissionDenied(current_user_id=current_user_id)
            except PostDoesNotExist:
                raise PostNotFoundByIdException(post_id=post_id)
            self._repo.delete_post(session=session, post=post)
