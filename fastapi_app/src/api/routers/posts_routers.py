from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.posts import PostRequest, PostUpdate, PostResponse
from domain.use_cases.posts_usecases import (
    GetPostUseCase,
    GetPostByIdUseCase,
    GetPostsByAuthorUseCase,
    GetPostsByCategoryUseCase,
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
)
from api.depends import (
    get_posts_use_case,
    get_post_by_id_use_case,
    get_posts_by_author_use_case,
    get_posts_by_category_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
)
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserPermisionException,
    CategoryNotFoundBySlugException,
)

router = APIRouter(prefix="/api/v1")


@router.get(
    "/posts",
    status_code=status.HTTP_200_OK,
    response_model=List[PostResponse],
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
    status_code=status.HTTP_200_OK,
    response_model=PostResponse,
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
            detail=exc.detail,
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        )


@router.get(
    "/authors/{login}/posts",
    status_code=status.HTTP_200_OK,
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
    status_code=status.HTTP_200_OK,
    response_model=List[PostResponse],
)
async def get_posts_by_category(
    category_slug: str,
    skip: int = 0,
    limit: int = 10,
    use_case: GetPostsByCategoryUseCase = Depends(get_posts_by_category_use_case),
) -> List[PostResponse]:
    try:
        return await use_case.execute(category_slug=category_slug, skip=skip, limit=limit)
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.post(
    "/posts/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
)
async def create_post(
    post: PostRequest,
    author_id: int,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(data=post, author_id=author_id)
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
    "/posts/{post_id}/edit",
    status_code=status.HTTP_200_OK,
    response_model=PostResponse,
)
async def update_post(
    post_id: int,
    post: PostUpdate,
    current_user_id: int,
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(
            post_id=post_id,
            data=post,
            current_user_id=current_user_id,
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


@router.delete(
    "/posts/{post_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: int,
    current_user_id: int,
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
) -> None:
    try:
        await use_case.execute(post_id=post_id, current_user_id=current_user_id)
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