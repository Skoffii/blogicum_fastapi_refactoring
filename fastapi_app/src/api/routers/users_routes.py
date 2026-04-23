from fastapi import APIRouter, status, HTTPException, Depends

from schemas.users import UserRequest, UserUpdate, UserResponse
from domain.use_cases.user_usecase import (
    GetUserByIdUseCase,
    GetUserByLoginUseCase,
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from api.depends import (
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    create_user_use_case,
    update_user_use_case,
    delete_user_use_case,
)
from core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserAlreadyExistExeption,
    UserEmailIsNotUniqueException,
    UserPermisionException,
)

router = APIRouter()


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.get(
    "/users/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_login(
    login: str,
    use_case: GetUserByLoginUseCase = Depends(get_user_by_login_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )


@router.post(
    "/users/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    user: UserRequest,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(data=user)
    except UserAlreadyExistExeption as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        )
    except UserEmailIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        )


@router.put(
    "/user/{user_id}/edit",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    use_case: UpdateUserUseCase = Depends(update_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id, data=user)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )
    except UserEmailIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        )


@router.delete(
    "/user/{user_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    current_user_id: int,
    use_case: DeleteUserUseCase = Depends(delete_user_use_case),
) -> None:
    try:
        await use_case.execute(user_id=user_id, current_user_id=current_user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        )
    except UserPermisionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        )