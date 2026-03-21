from fastapi import APIRouter, status, Depends
from typing import List

from schemas.posts import PostRequest, PostUpdate, PostResponse
from domain.use_cases.posts_usecases import *
from api.depends import (
    get_posts_use_case,
    get_post_by_id_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def index(
    use_case: GetPostUseCase = Depends(get_posts_use_case),
) -> List[PostResponse]:
    return await use_case.execute()


@router.get(
    "/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse
)
async def post_detail(
    post_id: int, use_case: GetPostByIdUseCase = Depends(get_post_by_id_use_case)
) -> PostResponse:
    post = await use_case.execute(post_id=post_id)
    return post


@router.post(
    "/posts/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create_post(
    post: PostRequest,
    user: int = 1,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponse:
    new_post = await use_case.execute(author_id=user, data=post)
    return new_post


@router.put(
    "/posts/{post_id}/edit", status_code=status.HTTP_200_OK, response_model=PostResponse
)
async def edit_post(
    post_id: int,
    post: PostUpdate,
    user: int,
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponse:
    updated_post = await use_case.execute(
        post_id=post_id, data=post, current_user_id=user
    )
    return updated_post


@router.delete("/posts/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user_id: int,  # После добавления авторизации нужно будет изменить
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
) -> None:
    await use_case.execute(post_id=post_id, current_user_id=user_id)
    return None
