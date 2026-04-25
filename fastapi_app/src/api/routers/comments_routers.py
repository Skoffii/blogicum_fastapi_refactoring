from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from fastapi import UploadFile, File

from schemas.comments import CommentRequest, CommentUpdate, CommentResponse, CommentImageResponse
from schemas.error import ErrorResponse, ValidationErrorResponse
from domain.use_cases.comment_usecase import (
    GetCommentByIdUseCase,
    GetCommentsByPostUseCase,
    CreateCommentUseCase,
    UpdateCommentUseCase,
    DeleteCommentUseCase,
    GetCommentImageUseCase,
    AddCommentImageUseCase,
)
from api.depends import (
    get_comment_by_id_use_case,
    get_comments_by_post_use_case,
    create_comment_use_case,
    update_comment_use_case,
    delete_comment_use_case,
    get_comment_image_use_case,
    add_comment_image_use_case,
)
from core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    UserPermisionException,
    PostNotFoundByIdException,
    CommentHasNoImageException,
)

router = APIRouter()


@router.get(
    "posts/{post_id}/comments/{comment_id}",
    response_model=CommentResponse,
    responses={
        200: {"model": CommentResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_comment_by_id(
    post_id: int,
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_comment_by_id_use_case),
) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/posts/{post_id}/comments",
    response_model=List[CommentResponse],
    responses={
        200: {"model": List[CommentResponse]},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
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
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/posts/{comment_id}/images",
    response_model=CommentImageResponse,
    responses={
        200: {"model": CommentImageResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_post_image(
    comment_id: int,
    use_case: GetCommentImageUseCase = Depends(get_comment_image_use_case),
) -> CommentImageResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentHasNoImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.post(
    "/posts/{post_id}/comments/{comment_id}",
    response_model=CommentResponse,
    responses={
        201: {"model": CommentResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
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
            detail=exc.get_detail(),
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

@router.post(
    "/posts/{post_id}/comments/{comment_id}/image",
    response_model=CommentImageResponse,
    responses={
        201: {"model": CommentImageResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def add_comment_image(
    comment_id: int,
    post_id: int,
    image: UploadFile = File(...),
    use_case: AddCommentImageUseCase = Depends(add_comment_image_use_case),
) -> CommentImageResponse:
    try:
        return await use_case.execute(image=image, comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except CommentHasNoImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.put(
    "posts/{post_id}/comments/{comment_id}",
    response_model=CommentResponse,
    responses={
        200: {"model": CommentResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_comment(
    comment_id: int,
    post_id: int,
    comment: CommentUpdate,
    current_user_id: int,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
) -> CommentResponse:
    try:
        return await use_case.execute(
            comment_id=comment_id,
            post_id=post_id,
            data=comment,
            current_user_id=current_user_id,
        )
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail(),
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.delete(
    "/comments/{comment_id}/delete",
    responses={
        204: {"detail": "NO_CONTENT"},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
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
            detail=exc.detail(),
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

