from typing import Type, List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from models.comments_model import Comment
from schemas.comments import CommentRequest, CommentUpdate


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_comments_by_post(
            self, session: Session, post_id: int
            ) -> List[Comment]:
        query = (
            session.query(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        return query.all()

    def get_comment(
            self, session: Session, comment_id: int
            ) -> Optional[Comment]:
        query = (
            session.query(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.id == comment_id)
        )
        return query.scalar()

    def create_comment(
        self, session: Session, data: CommentRequest,
        author_id: int, post_id: int
    ) -> Comment:
        new_comment = self._model(
            data.model_dump(),
            author_id=author_id,
            post_id=post_id,
            pub_date=datetime.now,
        )
        session.add(new_comment)
        session.commit
        session.refresh(new_comment)
        return new_comment

    def update_comment(
        self, session: Session, comment: Comment, data: CommentUpdate
    ) -> Comment:
        up_comm = data.model_dump(exclude_unset=True)
        for key, value in up_comm.items():
            setattr(comment, key, value)
        session.commit
        session.refresh(comment)
        return comment

    def delete_comment(self, session: Session, comment: Comment) -> None:
        session.delete(comment)
        session.commit()
