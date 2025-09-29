from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.openapi import openapi_extra
from src.api.users.schemas import (
    CandidateUserRegistrationRequest,
    HRUserRegistrationRequest,
    UserDetailedResponse,
    UserLoginRequest,
    UserMissionResponse,
    UserResponse,
    UsersListResponse,
    UserTokenResponse,
)
from src.core.artifacts.use_cases import (
    AddArtifactToUserUseCase,
    RemoveArtifactFromUserUseCase,
)
from src.core.missions.use_cases import GetMissionWithUserTasksUseCase
from src.core.users.use_cases import (
    AddCompetencyToUserUseCase,
    AddSkillToUserUseCase,
    CreateUserUseCase,
    GetUserWithRelationsUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
    RemoveCompetencyFromUserUseCase,
    RemoveSkillFromUserUseCase,
    UpdateUserCompetencyLevelUseCase,
    UpdateUserSkillLevelUseCase,
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
    description="Возвращает данные авторизованного пользователя с рангом и артефактами",
)
async def get_me(
    user: FromDishka[JwtUser], use_case: FromDishka[GetUserWithRelationsUseCase]
) -> UserDetailedResponse:
    user_data = await use_case.execute(login=user.login)
    return UserDetailedResponse.from_schema(user=user_data)


@router.get(
    path="/users",
    openapi_extra=openapi_extra,
    summary="Получить список пользователей",
    description="Возвращает список всех пользователей в системе",
)
async def list_users(
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[ListUsersUseCase],
) -> UsersListResponse:
    _ = user
    users = await use_case.execute()
    return UsersListResponse.from_schema(users)


@router.get(
    path="/users/{user_login}",
    openapi_extra=openapi_extra,
    summary="Получить информацию о пользователе",
    description="Возвращает детальную информацию о конкретном пользователе",
)
async def get_user(
    user_login: str,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[GetUserWithRelationsUseCase],
) -> UserDetailedResponse:
    _ = user
    user_data = await use_case.execute(login=user_login)
    return UserDetailedResponse.from_schema(user=user_data)


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


@router.post(
    path="/users/{user_login}/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить компетенцию пользователю",
    description="Добавляет компетенцию указанному пользователю с заданным уровнем",
)
async def add_competency_to_user(
    use_case: FromDishka[AddCompetencyToUserUseCase],
    user: FromDishka[JwtHRUser],
    user_login: str,
    competency_id: int,
    level: int = 0,
) -> Response:
    _ = user
    await use_case.execute(user_login=user_login, competency_id=competency_id, level=level)
    return Response(status_code=status.HTTP_201_CREATED)


@router.put(
    path="/users/{user_login}/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить уровень компетенции пользователя",
    description="Обновляет уровень компетенции у указанного пользователя",
)
async def update_user_competency_level(
    user_login: str,
    competency_id: int,
    level: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[UpdateUserCompetencyLevelUseCase],
) -> Response:
    _ = user
    await use_case.execute(user_login=user_login, competency_id=competency_id, level=level)
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    path="/users/{user_login}/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить компетенцию у пользователя",
    description="Убирает компетенцию у указанного пользователя",
)
async def remove_competency_from_user(
    user_login: str,
    competency_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveCompetencyFromUserUseCase],
) -> Response:
    _ = user
    await use_case.execute(user_login=user_login, competency_id=competency_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    path="/users/{user_login}/competencies/{competency_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить скил пользователю в компетенции",
    description="Добавляет скил указанному пользователю в рамках компетенции с заданным уровнем",
)
async def add_skill_to_user(
    use_case: FromDishka[AddSkillToUserUseCase],
    user: FromDishka[JwtHRUser],
    user_login: str,
    competency_id: int,
    skill_id: int,
    level: int = 0,
) -> Response:
    _ = user
    await use_case.execute(
        user_login=user_login, skill_id=skill_id, competency_id=competency_id, level=level
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.put(
    path="/users/{user_login}/competencies/{competency_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить уровень скила пользователя в компетенции",
    description="Обновляет уровень скила у указанного пользователя в рамках компетенции",
)
async def update_user_skill_level(
    user_login: str,
    competency_id: int,
    skill_id: int,
    level: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[UpdateUserSkillLevelUseCase],
) -> Response:
    _ = user
    await use_case.execute(
        user_login=user_login, skill_id=skill_id, competency_id=competency_id, level=level
    )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    path="/users/{user_login}/competencies/{competency_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить скил у пользователя в компетенции",
    description="Убирает скил у указанного пользователя в рамках компетенции",
)
async def remove_skill_from_user(
    user_login: str,
    competency_id: int,
    skill_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveSkillFromUserUseCase],
) -> Response:
    _ = user
    await use_case.execute(user_login=user_login, skill_id=skill_id, competency_id=competency_id)
    return Response(status_code=status.HTTP_200_OK)
