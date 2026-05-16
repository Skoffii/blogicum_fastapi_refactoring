from typing import List, Optional
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi import UploadFile
from uuid import uuid4
import shutil
import os
import logging

from infrastructure.database import database
from infrastructure.repos.post_rep import PostRepository
from infrastructure.repos.user_rep import UserRepository
from infrastructure.repos.category_rep import CategoryRepository
from schemas.posts import PostRequest, PostResponse, PostUpdate, PostImageResponse
from schemas.users import UserResponse
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


logger = logging.getLogger(__name__)

class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, skip: int = 0, limit: int = 20) -> List[PostResponse]:
        async with self._database.session() as session:
            posts = await self._repo.get_posts(session=session, skip=skip, limit=limit)
        return [PostResponse.model_validate(obj=post) for post in posts]


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, cur_user_id: Optional[int] = None
    ) -> PostResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session=session, post_id=post_id)

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
                error = UserPermissionDenied(cur_user_id=cur_user_id)
                logger.error(error.get_detail())
                raise error
            except PostNotFoundById:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            return PostResponse.model_validate(obj=post)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, login: str, skip: int = 0, limit: int = 10) -> dict:
        async with self._database.session() as session:
            user = await self._user_repo.get_by_login(session=session, login=login)
            try:
                posts = await self._repo.get_by_author(
                    session=session, author_id=user.id, skip=skip, limit=limit
                )
            except UserDoesNotExist:
                error = UserNotFoundByUsernameException(username=login)
                logger.error(error.get_detail())
                raise error
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
        async with self._database.session() as session:
            try:
                category = await self._category_repo.get_by_slug(
                    session=session, slug=category_slug
                )
            except CategoryNotFoundByName:
                error = CategoryNotFoundBySlugException(category_slug=category_slug)
                logger.error(error.get_detail())
                raise error
            posts = await self._repo.get_by_category(
                session=session, category_id=category.id, skip=skip, limit=limit
            )
            return [PostResponse.model_validate(obj=post) for post in posts]


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequest, author_id: int) -> PostResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.create_post(
                    session=session, data=data, author_id=author_id
                )
            except UserNotFoundById:
                error = UserNotFoundByIdException(user_id=author_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundByName:
                error = CategoryNotFoundBySlugException(category_slug=data.category_slug)
                logger.error(error.get_detail())
                raise error
            except CategoryNotPublished:
                error = CategoryNotFoundBySlugException(category_slug=data.category_slug)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(post)
            logger.info(
                    f"Пост {post.id} создан пользователем {author_id}",
                    extra={
                        "event": "post_created"
                    }
                )
            return PostResponse.model_validate(obj=post)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, data: PostUpdate, current_user_id: int
    ) -> PostResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session=session, post_id=post_id)

                if current_user_id != post.author_id:
                    raise PostAccessDenied
            except PostAccessDenied:
                error = UserPermisionException(current_user_id=current_user_id)
                logger.error(error.get_detail())
                raise error
            except PostDoesNotExist:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            try:
                post = await self._repo.update_post(session=session, post=post, data=data)
            except LocationNotFoundByName:
                error = LocationNotFoundByNameException(location_name=data.location_name)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundByName:
                error = CategoryNotFoundBySlugException(category_slug=data.category_slug)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(post)
            logger.info(
                    f"Пост {post.id} обновлен пользователем {current_user_id}",
                    extra={
                        "event": "post_updated"
                    }
                )
            return PostResponse.model_validate(obj=post)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, current_user_id: int) -> None:
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session=session, post_id=post_id)
                if current_user_id != post.author_id:
                    raise PostAccessDenied
            except PostAccessDenied:
                error = UserPermissionDenied(current_user_id=current_user_id)
                logger.error(error.get_detail())
                raise error
            except PostDoesNotExist:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            logger.info(
                    f"Пост {post.id} удален пользователем {current_user_id}",
                    extra={
                        "event": "post_deleted"
                    }
                )
            await self._repo.delete_post(session=session, post=post)


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self.image_folder = "./../images"

    async def execute(self, post_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                post = await self._repo.get_by_id(session=session, post_id=post_id)
        except PostNotFoundById:
            error = PostNotFoundByIdException(post_id=post_id)
            logger.error(error.get_detail())
            raise error

        if not post.image:
            error = PostHasNoImageException()
            logger.error(error.get_detail())
            raise error

        full_image_path: str = f"{self.image_folder}/{post.image}"
        return FileResponse(full_image_path, media_type="image/jpeg")


class AddPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self.image_folder = "./../images"

    async def execute(
        self, image: UploadFile, post_id: int, current_user_id: int
    ) -> PostImageResponse:
        os.makedirs(self.image_folder, exist_ok=True)
        if not image.filename or image.filename.split(".")[-1].lower() not in [
            "jpeg",
        ]:
            raise UploadFileIsNotImageException()
        file_extension = image.filename.split(".")[-1]
        new_image_name: str = f"{uuid4().hex}.{file_extension}"
        new_image_path: str = f"{self.image_folder}/{new_image_name}"
        with open(new_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session=session, post_id=post_id)
                if post.author_id != current_user_id:
                    error = UserPermisionException(current_user_id=current_user_id)
                    logger.error(error.get_detail())
                    raise error
            except PostNotFoundById:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            await self._repo.update_post_image(
                session=session, post_id=post.id, image_filename=new_image_name
            )
            await session.commit()
            await session.refresh(post)
        logger.info(
                    f"К посту {post.id} добавлено изображение пользователем {current_user_id}",
                    extra={
                        "event": "post_image_updated"
                    }
                )
        return PostImageResponse(image=new_image_name)
