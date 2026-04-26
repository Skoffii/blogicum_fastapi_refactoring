from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from typing import List

from schemas.posts import PostRequest, PostUpdate, PostResponse, PostImageResponse
from schemas.error import *
from domain.use_cases.posts_usecases import (
    GetPostUseCase,
    GetPostByIdUseCase,
    GetPostsByAuthorUseCase,
    GetPostsByCategoryUseCase,
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    GetPostImageUseCase,
    AddPostImageUseCase,
)
from api.depends import (
    get_posts_use_case,
    get_post_by_id_use_case,
    get_posts_by_author_use_case,
    get_posts_by_category_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
    get_post_image_use_case,
    add_post_image_use_case,
    get_current_user,
)
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserPermisionException,
    UserNotFoundByIdException,
    CategoryNotFoundBySlugException,
    PostHasNoImageException,
)
from schemas.auth import UserData

router = APIRouter()


@router.get(
    "/posts/",
    response_model=List[PostResponse],
    responses={
        200: {"model": PostResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_posts(
    skip: int = 0,
    limit: int = 20,
    use_case: GetPostUseCase = Depends(get_posts_use_case),
) -> List[PostResponse]:
    try:
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    responses={
        200: {"model": PostResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_post_by_id(
    post_id: int,
    current_user_id: int = None,
    use_case: GetPostByIdUseCase = Depends(get_post_by_id_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id, cur_user_id=current_user_id)
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


@router.get(
    "/authors/{login}/posts",
    response_model=PostResponse,
    responses={
        200: {"model": PostResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_posts_by_author(
    login: str,
    skip: int = 0,
    limit: int = 10,
    use_case: GetPostsByAuthorUseCase = Depends(get_posts_by_author_use_case),
) -> dict:
    try:
        return await use_case.execute(login=login, skip=skip, limit=limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/categories/{category_slug}/posts",
    response_model=List[PostResponse],
    responses={
        200: {"model": PostResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_posts_by_category(
    category_slug: str,
    skip: int = 0,
    limit: int = 10,
    use_case: GetPostsByCategoryUseCase = Depends(get_posts_by_category_use_case),
) -> List[PostResponse]:
    try:
        return await use_case.execute(
            category_slug=category_slug, skip=skip, limit=limit
        )
    except CategoryNotFoundBySlugException as exc:
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
    "/posts/{post_id}/images",
    response_model=PostImageResponse,
    responses={
        200: {"model": PostResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_post_image(
    post_id: int,
    use_case: GetPostImageUseCase = Depends(get_post_image_use_case),
) -> PostImageResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except PostHasNoImageException as exc:
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
    "/posts/create",
    response_model=PostResponse,
    responses={
        201: {"model": PostResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_post(
    post: PostRequest,
    author: UserData = Depends(get_current_user),
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(data=post, author_id=author.id)
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


async def add_post_image(
    post_id: int,
    image: UploadFile = File(...),
    current_user: UserData = Depends(get_current_user),
    use_case: AddPostImageUseCase = Depends(add_post_image_use_case),
) -> PostImageResponse:
    try:
        return await use_case.execute(
            image=image, post_id=post_id, current_user_id=current_user.id
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except PostHasNoImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.put(
    "/posts/{post_id}/edit",
    response_model=PostResponse,
    responses={
        201: {"model": PostResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_post(
    post_id: int,
    post: PostUpdate,
    current_user: UserData = Depends(get_current_user),
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(
            post_id=post_id,
            data=post,
            current_user_id=current_user.id,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail(),
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.get_detail(),
        )
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.delete(
    "/posts/{post_id}/delete",
    responses={
        204: {"detail": "NO_CONTENT"},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_post(
    post_id: int,
    current_user: UserData = Depends(get_current_user),
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
) -> None:
    try:
        return await use_case.execute(post_id=post_id, current_user_id=current_user.id)
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
