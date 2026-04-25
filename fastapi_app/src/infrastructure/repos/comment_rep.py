from typing import Type, List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.models.posts_model import Post
from infrastructure.models.users_model import User
from infrastructure.models.comments_model import Comment
from schemas.comments import CommentRequest, CommentUpdate
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_comments_by_post(self, session: Session, post_id: int) -> List[Comment]:
        query = (
            session.query(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        return query.all()

    def get_comment(self, session: Session, comment_id: int) -> Optional[Comment]:
        query = (
            session.query(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFound
        return comment

    def create_comment(
        self,
        session: Session,
        data: CommentRequest,
        author_id: int,
        post_id: int,
    ) -> Comment:
        post = session.query(Post).where(Post.id == post_id).scalar()
        if not post:
            raise PostNotFoundById
        author = session.query(User).where(User.id == author_id).scalar()
        if not author:
            raise UserNotFoundById

        new_comment = self._model(
            **data.model_dump(), author_id=author_id, post_id=post_id
        )
        session.add(new_comment)
        session.flush()
        session.refresh(new_comment)
        return new_comment

    def update_comment(
        self, session: Session, comment: Comment, data: CommentUpdate
    ) -> Comment:
        up_comm = data.model_dump(exclude_unset=True)
        for key, value in up_comm.items():
            setattr(comment, key, value)
        if data.author:
            author = session.query(User).where(User.username == data.author)
            if not author:
                raise UserDoesNotExist

        session.commit
        session.refresh(comment)
        return comment

    def delete_comment(self, session: Session, comment: Comment) -> None:
        exist = self.get_by_id(session, comment.id)
        if not exist:
            raise CommentNotFound
        session.delete(comment)
        session.commit()

    def update_comment_image(
        self, session: Session, comment_id: int, image_filename: str
    ) -> Post:
        comment = self.get_comment(session=session, comment_id=comment_id)
        comment.image = image_filename
        session.flush()
        return comment
