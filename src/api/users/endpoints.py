from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.openapi import openapi_extra
from src.api.users.schemas import (
    CandidateUserRegistrationRequest,
    HRUserRegistrationRequest,
    UserLoginRequest,
    UserMissionResponse,
    UserResponse,
    UserTokenResponse,
)
from src.core.artifacts.use_cases import (
    AddArtifactToUserUseCase,
    RemoveArtifactFromUserUseCase,
)
from src.core.missions.use_cases import GetMissionWithUserTasksUseCase
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
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить артефакт пользователю",
    description="Назначает артефакт указанному пользователю",
)
async def add_artifact_to_user(
    user_login: str,
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddArtifactToUserUseCase],
) -> UserResponse:
    _ = user
    user_with_artifact = await use_case.execute(user_login=user_login, artifact_id=artifact_id)
    return UserResponse.from_schema(user=user_with_artifact)


@router.delete(
    path="/users/{user_login}/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить артефакт у пользователя",
    description="Убирает артефакт у указанного пользователя",
)
async def remove_artifact_from_user(
    user_login: str,
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveArtifactFromUserUseCase],
) -> UserResponse:
    _ = user
    user_with_artifact = await use_case.execute(user_login=user_login, artifact_id=artifact_id)
    return UserResponse.from_schema(user=user_with_artifact)


@router.get(
    path="/users/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить миссию пользователя",
    description="Возвращает миссию с задачами и статусом их выполнения для текущего пользователя",
)
async def get_user_mission(
    mission_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionWithUserTasksUseCase],
) -> UserMissionResponse:
    mission = await use_case.execute(mission_id=mission_id, user_login=user.login)
    return UserMissionResponse.from_schema(mission=mission)
