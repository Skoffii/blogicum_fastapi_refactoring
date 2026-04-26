from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token
from domain.use_cases.auth_usecases import (
    AuthenticateUserUseCase,
    CreateAccessTokenUseCase,
)
from api.depends import authenticate_user_use_case, create_access_token_use_case
from core.exceptions.domain_exceptions import (
    InvalidUsernameException,
    WrongPasswordException,
)

router = APIRouter()


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase, Depends(authenticate_user_use_case)
    ],
    token_use_case: CreateAccessTokenUseCase = Depends(create_access_token_use_case),
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=form_data.username, password=form_data.password
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
        )
    access_token = await token_use_case.execute(login=user.username)

    return Token(access_token=access_token, token_type="bearer")
