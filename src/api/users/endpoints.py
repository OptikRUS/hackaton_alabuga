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
    UserUpdateRequest,
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
    UpdateUserUseCase,
)

router = APIRouter(tags=["users"], route_class=DishkaRoute)


@router.post(
    path="/users/register",
    summary="Рegictraciya pol'zoBatelya",
    description="Сozdaet noBogo pol'zoBatelya B cicteme c ykazannymi dannymi",
)
async def register_user(
    body: HRUserRegistrationRequest,
    use_case: FromDishka[CreateUserUseCase],
) -> Response:
    await use_case.execute(user=body.to_schema())
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    path="/mobile/users/register",
    summary="Рegictraciya kandidata",
    description="Сozdaet noBogo kandidata B cicteme c ykazannymi dannymi",
)
async def register_candidate(
    body: CandidateUserRegistrationRequest,
    use_case: FromDishka[CreateUserUseCase],
) -> Response:
    await use_case.execute(user=body.to_schema())
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    path="/users/login",
    summary="Вhod B cictemy",
    description="Аytentifikaciya pol'zoBatelya i polychenie JWT tokena",
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
    summary="Пolychit' informaciyu o tekyshem pol'zoBatele",
    description="ВozBrashaet dannye aBtorizoBannogo pol'zoBatelya c rangom i artefaktami",
)
async def get_me(
    user: FromDishka[JwtUser], use_case: FromDishka[GetUserWithRelationsUseCase]
) -> UserDetailedResponse:
    user_data = await use_case.execute(login=user.login)
    return UserDetailedResponse.from_schema(user=user_data)


@router.get(
    path="/users",
    openapi_extra=openapi_extra,
    summary="Пolychit' cpicok pol'zoBatelej",
    description="ВozBrashaet cpicok Bceh pol'zoBatelej B cicteme",
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
    summary="Пolychit' informaciyu o pol'zoBatele",
    description="ВozBrashaet detal'nyyu informaciyu o konkretnom pol'zoBatele",
)
async def get_user(
    user_login: str,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[GetUserWithRelationsUseCase],
) -> UserDetailedResponse:
    _ = user
    user_data = await use_case.execute(login=user_login)
    return UserDetailedResponse.from_schema(user=user_data)


@router.put(
    path="/users/{user_login}",
    openapi_extra=openapi_extra,
    summary="О6noBit' 6azoByyu informaciyu pol'zoBatelya",
    description=(
        "О6noBlyaet 6azoByyu informaciyu pol'zoBatelya "
        "(imya, familiya, parol', mana, rang, opyt) "
        "6ez izmeneniya kompetencij, naBykoB i artefaktoB"
    ),
)
async def update_user(
    user_login: str,
    body: UserUpdateRequest,
    user: FromDishka[JwtHRUser],
    get_user_use_case: FromDishka[GetUserWithRelationsUseCase],
    update_user_use_case: FromDishka[UpdateUserUseCase],
) -> UserResponse:
    _ = user
    current_user = await get_user_use_case.execute(login=user_login)

    updated_user = body.to_schema(login=user_login, current_user=current_user)

    await update_user_use_case.execute(user=updated_user)

    updated_user_data = await get_user_use_case.execute(login=user_login)
    return UserResponse.from_schema(user=updated_user_data)


@router.post(
    path="/users/{user_login}/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Дo6aBit' artefakt pol'zoBatelyu",
    description="Нaznachaet artefakt ykazannomy pol'zoBatelyu",
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
    summary="Уdalit' artefakt y pol'zoBatelya",
    description="У6iraet artefakt y ykazannogo pol'zoBatelya",
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
    summary="Пolychit' micciyu pol'zoBatelya",
    description=(
        "ВozBrashaet micciyu c zadachami i ctatycom ih Bypolneniya dlya tekyshego pol'zoBatelya"
    ),
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
    summary="Дo6aBit' kompetenciyu pol'zoBatelyu",
    description="Дo6aBlyaet kompetenciyu ykazannomy pol'zoBatelyu c zadannym yroBnem",
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
    summary="О6noBit' yroBen' kompetencii pol'zoBatelya",
    description="О6noBlyaet yroBen' kompetencii y ykazannogo pol'zoBatelya",
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
    summary="Уdalit' kompetenciyu y pol'zoBatelya",
    description="У6iraet kompetenciyu y ykazannogo pol'zoBatelya",
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
    summary="Дo6aBit' ckil pol'zoBatelyu B kompetencii",
    description="Дo6aBlyaet ckil ykazannomy pol'zoBatelyu B ramkah kompetencii c zadannym yroBnem",
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
    summary="О6noBit' yroBen' ckila pol'zoBatelya B kompetencii",
    description="О6noBlyaet yroBen' ckila y ykazannogo pol'zoBatelya B ramkah kompetencii",
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
    summary="Уdalit' ckil y pol'zoBatelya B kompetencii",
    description="У6iraet ckil y ykazannogo pol'zoBatelya B ramkah kompetencii",
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
