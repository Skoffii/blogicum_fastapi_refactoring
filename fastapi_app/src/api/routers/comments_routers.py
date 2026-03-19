from fastapi import APIRouter, HTTPException, status
from test_db import db
from schemas.comments import CommentRequest, CommentUpdate, CommentResponse
from datetime import datetime

router = APIRouter(prefix="/posts/{post_id}")


@router.post(
    "/comment/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse
)
async def add_comment(post_id: int, comment: CommentRequest):
    global db
    for post in db.posts_db:
        if post["id"] == post_id:
            new_comment = comment.model_dump()
            new_comment["id"] = db.comment_id
            new_comment["post_id"] = post_id
            new_comment["created_at"] = datetime.now()
            db.comments_db.append(new_comment)
            db.comment_id += 1
            return new_comment
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.put(
    "/edit_comment/{comment_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def edit_comment(post_id: int, comment_id: int, comment: CommentUpdate):
    for post in db.posts_db:
        if post["id"] == post_id:
            for db_comment in db.comments_db:
                if db_comment["id"] == comment_id:
                    update_comment = comment.model_dump(exclude_unset=True)
                    db_comment.update(update_comment)
                    return db_comment
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/delete_comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(post_id: int, comment_id: int):
    for post in db.posts_db:
        if post["id"] == post_id:
            for comment_num, comment in enumerate(db.comments_db):
                if comment["id"] == comment_id:
                    db.comments_db.pop(comment_num)
                    return None
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
