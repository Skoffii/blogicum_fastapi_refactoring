from infrastructure.database import database
from infrastructure.repos.comment_rep import CommentRepository
from infrastructure.repos.post_rep import PostRepository
from schemas.comments import CommentRequest, CommentResponse, CommentUpdate
from fastapi import HTTPException, status
from typing import List
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
                    post_id=post_id
                )

                session.commit()
            except PostNotFoundById:
                raise PostNotFoundByIdException(post_id=post_id)
            except UserNotFoundById:
                raise UserNotFoundByIdException(user_id=str(author_id))

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
                    session=session, 
                    comment=comment, 
                    data=data
                )
            except CommentNotFoundById:
                raise CommentNotFoundByIdException(comment_id=comment_id)
            except UserPermisionException:
                raise 

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
            self._repo.delete_comment(session=session, comment=comment)
