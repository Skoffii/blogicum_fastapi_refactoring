from fastapi import APIRouter, status, Depends

from schemas.comments import CommentRequest, CommentUpdate, CommentResponse
from domain.use_cases.comment_usecase import *
from api.depends import (
    get_comments_by_post_use_case,
    get_comment_by_id_use_case,
    create_comment_use_case,
    update_comment_use_case,
    delete_comment_use_case,
)

router = APIRouter(prefix="/posts/{post_id}")


@router.get(
    "/comments/", status_code=status.HTTP_200_OK, response_model=List[CommentResponse]
)
async def get_post_commets(
    post_id: int,
    use_case: GetCommentsByPostUseCase = Depends(get_comments_by_post_use_case),
) -> CommentResponse:
    return await use_case.execute(post_id=post_id)


@router.get(
    "/comments/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def get_comment(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_comment_by_id_use_case),
) -> CommentResponse:
    comment = await use_case.execute(comment_id=comment_id)
    return comment


@router.post(
    "/comment/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse
)
async def add_comment(
    post_id: int,
    user: int,
    comment: CommentRequest,
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
) -> CommentResponse:
    new_comment = await use_case.execute(post_id=post_id, data=comment, author_id=user)
    return new_comment


@router.put(
    "/edit_comment/{comment_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def edit_comment(
    comment_id: int,
    user: int,
    comment: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
) -> CommentResponse:
    updated_comment = await use_case.execute(
        comment_id=comment_id, data=comment, current_user_id=user
    )
    return updated_comment


@router.delete("/delete_comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    user: int,
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
) -> None:
    await use_case.execute(comment_id=comment_id, current_user_id=user)
    return None
