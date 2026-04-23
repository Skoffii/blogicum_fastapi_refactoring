from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.comments import CommentRequest, CommentUpdate, CommentResponse
from domain.use_cases.comment_usecase import (
    GetCommentByIdUseCase,
    GetCommentsByPostUseCase,
    CreateCommentUseCase,
    UpdateCommentUseCase,
    DeleteCommentUseCase,
)
from api.depends import (
    get_comment_by_id_use_case,
    get_comments_by_post_use_case,
    create_comment_use_case,
    update_comment_use_case,
    delete_comment_use_case,
)
from core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    UserPermisionException,
    PostNotFoundByIdException,
)

router = APIRouter(prefix="/api/v1")


@router.get(
    "/comments/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_comment_by_id_use_case),
) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.get(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=List[CommentResponse],
)
async def get_comments_by_post(
    post_id: int,
    use_case: GetCommentsByPostUseCase = Depends(get_comments_by_post_use_case),
) -> List[CommentResponse]:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.post(
    "/posts/{post_id}/comments/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_comment(
    post_id: int,
    comment: CommentRequest,
    author_id: int,
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
) -> CommentResponse:
    try:
        return await use_case.execute(
            post_id=post_id,
            data=comment,
            author_id=author_id,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        )


@router.put(
    "/comments/{comment_id}/edit",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    current_user_id: int,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
) -> CommentResponse:
    try:
        return await use_case.execute(
            comment_id=comment_id,
            data=comment,
            current_user_id=current_user_id,
        )
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        )


@router.delete(
    "/comments/{comment_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: int,
    current_user_id: int,
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
) -> None:
    try:
        await use_case.execute(
            comment_id=comment_id,
            current_user_id=current_user_id,
        )
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        )