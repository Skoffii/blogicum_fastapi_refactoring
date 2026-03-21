from fastapi import APIRouter, status, Depends

from schemas.users import UserRequest, UserUpdate, UserResponse
from domain.use_cases.user_usecase import *
from api.depends import (
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    create_user_use_case,
    update_user_use_case,
    delete_user_use_case,
)

router = APIRouter()


@router.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def get_user_by_id(
    user_id: int, use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case)
) -> UserResponse:
    user = await use_case.execute(user_id=user_id)
    return user


@router.get("/users/{login}", status_code=status.HTTP_200_OK)
async def get_user_by_login(
    login: str, use_case: GetUserByLoginUseCase = Depends(get_user_by_login_use_case)
) -> UserResponse:
    user = await use_case.execute(login=login)
    return user


@router.post(
    "/users/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def create_user(
    user: UserRequest, use_case: CreateUserUseCase = Depends(create_user_use_case)
) -> UserResponse:
    new_user = await use_case.execute(data=user)
    return new_user


@router.put(
    "/user/{user_id}/edit", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    use_case: UpdateUserUseCase = Depends(update_user_use_case),
) -> UserResponse:
    updated_user = await use_case.execute(user_id=user_id, data=user)
    return updated_user


@router.delete("/user/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, user: int, use_case: DeleteUserUseCase = Depends(delete_user_use_case)
) -> None:
    await use_case.execute(
        user_id=user_id, current_user_id=user
    )  # с current user нужно решить после добавления аутетификации
    return None
