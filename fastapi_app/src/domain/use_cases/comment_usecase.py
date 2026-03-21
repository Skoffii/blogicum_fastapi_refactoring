from infrastructure.database import database
from infrastructure.repos.comment_rep import CommentRepository
from infrastructure.repos.post_rep import PostRepository
from schemas.comments import CommentRequest, CommentResponse, CommentUpdate
from fastapi import HTTPException, status
from typing import List


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.get_comment(session=session, comment_id=comment_id)
            if not comment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return CommentResponse.model_validate(obj=comment)


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> List[CommentResponse]:
        with self._database.session() as session:
            post = self._post_repo.get_by_id(session=session, post_id=post_id)
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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
            post = self._post_repo.get_by_id(session=session, post_id=post_id)

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            comment = self._repo.create_comment(
                session=session, data=data, author_id=author_id, post_id=post_id
            )

        return CommentResponse.model_validate(obj=comment)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, comment_id: int, data: CommentUpdate, current_user_id: int
    ) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.get_comment(session=session, comment_id=comment_id)

            if not comment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if current_user_id != comment.author_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

            comment = self._repo.update_comment(
                session=session, comment=comment, data=data
            )

        return CommentResponse.model_validate(obj=comment)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            comment = self._repo.get_comment(session=session, comment_id=comment_id)
            if not comment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if current_user_id != comment.author_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            self._repo.delete_comment(session=session, comment=comment)
