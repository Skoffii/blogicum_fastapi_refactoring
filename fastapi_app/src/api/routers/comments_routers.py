from fastapi import APIRouter, HTTPException, status
from src.test_db import posts_db, comments_db
from src.schemas.comments import CommentRequest, CommentUpdate, CommentResponse
from datetime import datetime

router = APIRouter(prefix="/posts/{post_id}")


@router.post(
    "/comment/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse
)
async def add_comment(post_id: int, comment: CommentRequest):
    global comment_id
    for post in posts_db:
        if post["id"] == post_id:
            new_comment = comment.model_dump
            new_comment["id"] = comment_id
            new_comment["post_id"] = post_id
            new_comment["created_at"] = datetime.now()
            comments_db.append(new_comment)
            comment_id += 1
            return new_comment
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.put(
    "/edit_comment/{comment_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def edit_comment(post_id: int, comment_id: int, comment: CommentUpdate):
    for post in posts_db:
        if post["id"] == post_id:
            for comment in comments_db:
                if comment["id"] == comment_id:
                    update_comment = post.model_dump(exclude_unset=True)
                    comment.update(update_comment)
                    return comment
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/delete_comment/{comemnt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comemnt(post_id: int, comment_id: int):
    for post in posts_db:
        if post["id"] == post_id:
            for comment_num, comment in enumerate(comments_db):
                if comment["id"] == comment_id:
                    comments_db.pop(comment_num)
                    return None
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
