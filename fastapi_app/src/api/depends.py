from domain.use_cases.posts_usecases import (
    GetPostUseCase,
    GetPostByIdUseCase,
    GetPostsByAuthorUseCase,
    GetPostsByCategoryUseCase,
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
)

from domain.use_cases.comment_usecase import (
    GetCommentsByPostUseCase,
    GetCommentByIdUseCase,
    CreateCommentUseCase,
    UpdateCommentUseCase,
    DeleteCommentUseCase,
)

from domain.use_cases.category_usecases import (
    GetCategoryByIdUseCase,
    GetCategoryBySlugUseCase,
)

from domain.use_cases.location_usecases import (
    GetLocationByIdUseCase
)

from domain.use_cases.user_usecase import (
    GetUserByIdUseCase,
    GetUserByLoginUseCase,
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)


async def get_posts_use_case() -> GetPostUseCase:
    return GetPostUseCase()


async def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


async def get_posts_by_author_use_case() -> GetPostsByAuthorUseCase:
    return GetPostsByAuthorUseCase()


async def get_posts_by_category_use_case() -> GetPostsByCategoryUseCase:
    return GetPostsByCategoryUseCase()


async def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


async def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


async def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


async def get_comments_by_post_use_case() -> GetCommentsByPostUseCase:
    return GetCommentsByPostUseCase()


async def get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()


async def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


async def update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()


async def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


async def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


async def get_category_by_slug_use_case() -> GetCategoryBySlugUseCase:
    return GetCategoryBySlugUseCase()


async def get_location_by_id() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()

async def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


async def get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


async def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


async def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


async def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()
