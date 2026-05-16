from fastapi.responses import FileResponse
from typing import List
from uuid import uuid4
import shutil
import os
from fastapi import UploadFile
import logging

from infrastructure.database import database
from infrastructure.repos.comment_rep import CommentRepository
from infrastructure.repos.post_rep import PostRepository
from schemas.comments import (
    CommentRequest,
    CommentResponse,
    CommentUpdate,
    CommentImageResponse,
)
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *

logger = logging.getLogger(__name__)

class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_comment(session=session, comment_id=comment_id)
            except CommentNotFound:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                logger.error(error.get_detail())
                raise error
            return CommentResponse.model_validate(comment)


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> List[CommentResponse]:
        async with self._database.session() as session:
            try:
                await self._post_repo.get_by_id(session=session, post_id=post_id)
            except PostNotFoundById:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            comments = await self._repo.get_comments_by_post(session=session, post_id=post_id)
            return [CommentResponse.model_validate(obj=comment) for comment in comments]


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(
        self, post_id: int, data: CommentRequest, author_id: int
    ) -> CommentResponse:
        async with self._database.session() as session:
            try:
                await self._post_repo.get_by_id(session=session, post_id=post_id)
                comment = await self._repo.create_comment(
                    session=session,
                    data=data,
                    author_id=author_id,
                    post_id=post_id,
                )
                session.commit()
            except PostNotFoundById:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.get_detail())
                raise error
            except UserNotFoundById:
                error = UserNotFoundByIdException(user_id=str(author_id))
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(comment)
            logger.info(
                    f"Комментарий {comment.id} создан пользователем {author_id}",
                    extra={
                        "event": "comment_created"
                    }
                )
            return CommentResponse.model_validate(obj=comment)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, comment_id: int, data: CommentUpdate, current_user_id: int
    ) -> CommentResponse:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_comment(session=session, comment_id=comment_id)
                if current_user_id != comment.author_id:
                    error = UserPermisionException(current_user_id=str(current_user_id))
                    logger.error(error.get_detail())
                    raise error
                updated_comment = self._repo.update_comment(
                    session=session, comment=comment, data=data
                )
            except CommentNotFound:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                logger.error(error.get_detail())
                raise error
            except UserPermissionDenied:
                error = UserPermisionException(current_user_id=current_user_id)
                logger.error(error.get_detail())
                raise error
            await session.commit()
            await session.refresh(comment)
            logger.info(
                    f"Комментарий {comment.id} обновлен пользователем {current_user_id}",
                    extra={
                        "event": "comment_updated"
                    }
                )
            return CommentResponse.model_validate(obj=updated_comment)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, current_user_id: int) -> None:
        async  with self._database.session() as session:
            comment = await self._repo.get_comment(session=session, comment_id=comment_id)
            try:
                if not comment:
                    raise CommentNotFound
                if current_user_id != comment.author_id:
                    raise UserPermissionDenied
            except CommentNotFound:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                logger.error(error.get_detail())
                raise error
            except UserPermissionDenied:
                error = UserPermisionException(current_user_id=current_user_id)
            await session.commit()
            await self._repo.delete_comment(session=session, comment=comment)
            logger.info(
                    f"Комментарий {comment.id} удален пользователем {current_user_id}",
                    extra={
                        "event": "comment_deleted"
                    }
                )


class GetCommentImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()
        self.image_folder = "./../images"

    async def execute(self, comment_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                comment = await self._repo.get_comment(session=session, comment_id=comment_id)
        except CommentNotFound:
            error = CommentNotFoundByIdException(comment_id=comment_id)
            logger.error(error.get_detail())
            raise error
        if not comment.image:
            error = CommentHasNoImageException()
            logger.error(error.get_detail())
            raise error
        full_image_path: str = f"{self.image_folder}/{comment.image}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")


class AddCommentImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()
        self.image_folder = "./../images"

    async def execute(
        self, comment_id: int, current_user_id: int, image: UploadFile
    ) -> CommentImageResponse:
        os.makedirs(self.image_folder, exist_ok=True)
        if not image.filename or image.filename.split(".")[-1].lower() not in ["jpeg"]:
            raise UploadFileIsNotImageException()
        new_image_name: str = f"{uuid4().hex}"
        new_image_path: str = f"{self.image_folder}/{new_image_name}.jpeg"
        with open(new_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_comment(session=session, comment_id=comment_id)
                if comment.author_id != current_user_id:
                    error = UserPermisionException(current_user_id=current_user_id)
                    logger.error(error.get_detail())
                    raise error
            except CommentNotFound:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                logger.error(error.get_detail())
                raise error
            self._repo.update_comment_image(
                session=session, comment_id=comment_id, image_filename=new_image_name
            )
            await session.commit()
            await session.refresh(comment)
            logger.info(
                    f"К комментарию {comment.id} добавлено изображение пользователем {current_user_id}",
                    extra={
                        "event": "comment_image_updated"
                    }
                )
            return CommentImageResponse(image=new_image_name)
