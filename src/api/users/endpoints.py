from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response, status

from src.api.auth.schemas import JwtUser
from src.api.openapi import openapi_extra
from src.api.users.schemas import (
    UserLoginRequest,
    UserRegistrationRequest,
    UserResponse,
    UserTokenResponse,
)
from src.core.users.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    LoginUserUseCase,
)

router = APIRouter(tags=["users"], route_class=DishkaRoute)


@router.post(path="/users/register")
async def register_user(
    body: UserRegistrationRequest,
    use_case: FromDishka[CreateUserUseCase],
) -> Response:
    await use_case.execute(user=body.to_schema())
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(path="/users/login")
async def user_login(
    body: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
) -> UserTokenResponse:
    token = await use_case.execute(login=body.login, password=body.password)
    return UserTokenResponse(token=token)


@router.get(path="/users/me", openapi_extra=openapi_extra)
async def get_me(user: FromDishka[JwtUser], use_case: FromDishka[GetUserUseCase]) -> UserResponse:
    registered_user = await use_case.execute(login=user.login)
    return UserResponse.from_schema(user=registered_user)
