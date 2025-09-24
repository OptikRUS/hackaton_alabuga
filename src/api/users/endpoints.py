from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response, status

from src.api.auth.schemas import JwtUser
from src.api.openapi import openapi_extra
from src.api.users.schemas import (
    CandidateUserRegistrationRequest,
    HRUserRegistrationRequest,
    UserLoginRequest,
    UserResponse,
    UserTokenResponse,
)
from src.core.artifacts.use_cases import (
    AddArtifactToUserUseCase,
    RemoveArtifactFromUserUseCase,
)
from src.core.users.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    LoginUserUseCase,
)

router = APIRouter(tags=["users"], route_class=DishkaRoute)


@router.post(
    path="/users/register",
    summary="Регистрация пользователя",
    description="Создает нового пользователя в системе с указанными данными",
)
async def register_user(
    body: HRUserRegistrationRequest,
    use_case: FromDishka[CreateUserUseCase],
) -> Response:
    await use_case.execute(user=body.to_schema())
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    path="/mobile/users/register",
    summary="Регистрация кандидата",
    description="Создает нового кандидата в системе с указанными данными",
)
async def register_candidate(
    body: CandidateUserRegistrationRequest,
    use_case: FromDishka[CreateUserUseCase],
) -> Response:
    await use_case.execute(user=body.to_schema())
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    path="/users/login",
    summary="Вход в систему",
    description="Аутентификация пользователя и получение JWT токена",
)
async def user_login(
    body: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
) -> UserTokenResponse:
    token = await use_case.execute(login=body.login, password=body.password)
    return UserTokenResponse(token=token)


@router.get(
    path="/users/me",
    openapi_extra=openapi_extra,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает данные авторизованного пользователя",
)
async def get_me(user: FromDishka[JwtUser], use_case: FromDishka[GetUserUseCase]) -> UserResponse:
    registered_user = await use_case.execute(login=user.login)
    return UserResponse.from_schema(user=registered_user)


@router.post(
    path="/users/{user_login}/artifacts/{artifact_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить артефакт пользователю",
    description="Назначает артефакт указанному пользователю",
)
async def add_artifact_to_user(
    user_login: str,
    artifact_id: int,
    use_case: FromDishka[AddArtifactToUserUseCase],
) -> UserResponse:
    user = await use_case.execute(user_login=user_login, artifact_id=artifact_id)
    return UserResponse.from_schema(user=user)


@router.delete(
    path="/users/{user_login}/artifacts/{artifact_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить артефакт у пользователя",
    description="Убирает артефакт у указанного пользователя",
)
async def remove_artifact_from_user(
    user_login: str,
    artifact_id: int,
    use_case: FromDishka[RemoveArtifactFromUserUseCase],
) -> UserResponse:
    user = await use_case.execute(user_login=user_login, artifact_id=artifact_id)
    return UserResponse.from_schema(user=user)
