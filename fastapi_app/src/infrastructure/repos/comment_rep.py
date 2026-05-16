from typing import Type, List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.models.posts_model import Post
from infrastructure.models.users_model import User
from infrastructure.models.comments_model import Comment
from schemas.comments import CommentRequest, CommentUpdate
from core.exceptions.infrastructure_exceptions import *
from core.exceptions.domain_exceptions import *


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    async def get_comments_by_post(self, session: AsyncSession, post_id: int) -> List[Comment]:
        query = await session.execute(
            select(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        return query.scalars().all()

    async def get_comment(self, session: AsyncSession, comment_id: int) -> Optional[Comment]:
        query = await session.execute(
            select(self._model)
            .options(joinedload(self._model.author))
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFound
        return comment

    async def create_comment(
        self,
        session: AsyncSession,
        data: CommentRequest,
        author_id: int,
        post_id: int,
    ) -> Comment:
        get_post = await session.execute(select(Post).where(Post.id == post_id))
        post = get_post.scalar()
        if not post:
            raise PostNotFoundById
        get_author = await session.execute(select(User).where(User.id == author_id))
        author = get_author.scalar()
        if not author:
            raise UserNotFoundById

        new_comment = self._model(
            **data.model_dump(), author_id=author_id, post_id=post_id
        )
        session.add(new_comment)
        await session.flush()
        await session.refresh(new_comment)
        return new_comment

    async def update_comment(
        self, session: AsyncSession, comment: Comment, data: CommentUpdate
    ) -> Comment:
        up_comm = data.model_dump(exclude_unset=True)
        for key, value in up_comm.items():
            setattr(comment, key, value)
        if data.author:
            get_author = await session.execute(select(User).where(User.username == data.author))
            author = get_author.scalar()
            if not author:
                raise UserDoesNotExist

        await session.commit
        await session.refresh(comment)
        return comment

    async def delete_comment(self, session: AsyncSession, comment: Comment) -> None:
        exist = await self.get_by_id(session, comment.id)
        if not exist:
            raise CommentNotFound
        await session.delete(comment)
        await session.commit()

    async def update_comment_image(
        self, session: AsyncSession, comment_id: int, image_filename: str
    ) -> Post:
        comment = await self.get_comment(session=session, comment_id=comment_id)
        comment.image = image_filename
        await session.flush()
        return comment
