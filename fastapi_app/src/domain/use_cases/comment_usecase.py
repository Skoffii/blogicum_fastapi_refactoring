from fastapi.responses import FileResponse
from typing import List
from uuid import uuid4
import shutil
import os
from fastapi import UploadFile


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


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        with self._database.session() as session:
            try:
                comment = self._repo.get_comment(session=session, comment_id=comment_id)
            except CommentNotFound:
                raise CommentNotFoundByIdException(comment_id=comment_id)
        return CommentResponse.model_validate(comment)


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> List[CommentResponse]:
        with self._database.session() as session:
            try:
                self._post_repo.get_by_id(session=session, post_id=post_id)
            except PostNotFoundById:
                raise PostNotFoundByIdException(post_id=post_id)

            comments = self._repo.get_comments_by_post(session=session, post_id=post_id)

        return [CommentResponse.model_validate(obj=comment) for comment in comments]


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(
        self, post_id: int, data: CommentRequest, author_id: int
    ) -> CommentResponse:
        with self._database.session() as session:
            try:
                self._post_repo.get_by_id(session=session, post_id=post_id)
                comment = self._repo.create_comment(
                    session=session,
                    data=data,
                    author_id=author_id,
                    post_id=post_id,
                )
                session.commit()
            except PostNotFoundById:
                raise PostNotFoundByIdException(post_id=post_id)
            except UserNotFoundById:
                raise UserNotFoundByIdException(user_id=str(author_id))
            session.commit()
            session.refresh(comment)
        return CommentResponse.model_validate(obj=comment)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, comment_id: int, data: CommentUpdate, current_user_id: int
    ) -> CommentResponse:
        with self._database.session() as session:
            try:
                comment = self._repo.get_comment(session=session, comment_id=comment_id)
                if current_user_id != comment.author_id:
                    raise UserPermisionException(current_user_id=str(current_user_id))
                updated_comment = self._repo.update_comment(
                    session=session, comment=comment, data=data
                )
            except CommentNotFound:
                raise CommentNotFoundByIdException(comment_id=comment_id)
            except UserPermissionDenied:
                raise UserPermisionException(current_user_id=current_user_id)
            session.commit()
            session.refresh(comment)
        return CommentResponse.model_validate(obj=updated_comment)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            comment = self._repo.get_comment(session=session, comment_id=comment_id)
            try:
                if not comment:
                    raise CommentNotFound
                if current_user_id != comment.author_id:
                    raise UserPermissionDenied
            except CommentNotFound:
                raise CommentNotFoundByIdException(comment_id=comment_id)
            except UserPermissionDenied:
                raise UserPermisionException(current_user_id=current_user_id)
            session.commit()
            self._repo.delete_comment(session=session, comment=comment)


class GetCommentImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()
        self.image_folder = "./../images"

    async def execute(self, comment_id: int) -> FileResponse:
        try:
            with self._database.session() as session:
                comment = self._repo.get_comment(session=session, comment_id=comment_id)
        except CommentNotFound:
            raise CommentNotFoundByIdException(comment_id=comment_id)

        if not comment.image:
            raise CommentHasNoImageException()
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
        with self._database.session() as session:
            try:
                comment = self._repo.get_comment(session=session, comment_id=comment_id)
                if comment.author_id != current_user_id:
                    raise UserPermisionException(current_user_id=current_user_id)
            except CommentNotFound:
                raise CommentNotFoundByIdException(comment_id=comment_id)
            self._repo.update_comment_image(
                session=session, comment_id=comment_id, image_filename=new_image_name
            )
            session.commit()
            session.refresh(comment)
        return CommentImageResponse(image=new_image_name)
