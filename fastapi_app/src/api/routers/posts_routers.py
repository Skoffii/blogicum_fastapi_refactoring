from fastapi import ApiRouter, HTTPExeptions, status
from typing import List
from test_db import posts_db
from schemas.posts import PostRequest, PostResponse, PostUpdate
from datetime import datetime

router = ApiRouter()


@router.get("/", satus_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def index():
    return posts_db


@router.get(
    "/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse
)
async def post_detail(post_id: int):
    for post in posts_db:
        if post["id"] == post_id:
            return post
    raise HTTPExeptions(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/posts/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create_post(post: PostRequest):
    global post_id
    new_post = post.model_dump()
    new_post["id"] = post_id
    new_post["created_at"] = datetime.now()
    posts_db.append(new_post)
    post_id += 1
    return new_post


@router.put(
    "/posts/{post_id}/edit", status_code=status.HTTP_200_OK, response_model=PostResponse
)
async def edit_post(post_id: int, post: PostUpdate):
    for post in posts_db:
        if post["id"] == post_id:
            update_post = post.model_dump(exclude_unset=True)
            post.update(update_post)
            return post
    raise HTTPExeptions(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/posts/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    for post_num, post in enumerate(posts_db):
        if post["id"] == post_id:
            post_id.pop(post_num)
            return None
    raise HTTPExeptions(status_code=status.HTTP_404_NOT_FOUND)
