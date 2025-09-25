from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.missions.schemas import (
    CompetencyRewardAddRequest,
    MissionCreateRequest,
    MissionResponse,
    MissionsResponse,
    MissionUpdateRequest,
    SkillRewardAddRequest,
)
from src.api.openapi import openapi_extra
from src.core.artifacts.use_cases import (
    AddArtifactToMissionUseCase,
    RemoveArtifactFromMissionUseCase,
)
from src.core.missions.use_cases import (
    AddCompetencyRewardToMissionUseCase,
    AddSkillRewardToMissionUseCase,
    AddTaskToMissionUseCase,
    CreateMissionUseCase,
    DeleteMissionUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveCompetencyRewardFromMissionUseCase,
    RemoveSkillRewardFromMissionUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionUseCase,
)

router = APIRouter(tags=["missions"], route_class=DishkaRoute)


@router.post(
    path="/missions",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать миссию",
    description="Создает новую миссию в системе",
)
async def create_mission(
    user: FromDishka[JwtHRUser],
    body: MissionCreateRequest,
    use_case: FromDishka[CreateMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission=body.to_schema())
    return MissionResponse.from_schema(mission=mission)


@router.get(
    path="/missions",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список миссий",
    description="Возвращает все доступные миссии",
)
async def get_missions(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionsUseCase],
) -> MissionsResponse:
    _ = user
    missions = await use_case.execute()
    return MissionsResponse.from_schema(missions=missions)


@router.get(
    path="/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить миссию по ID",
    description="Возвращает детальную информацию о миссии",
)
async def get_mission(
    mission_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionDetailUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id)
    return MissionResponse.from_schema(mission=mission)


@router.put(
    path="/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить миссию",
    description="Обновляет данные указанной миссии",
)
async def update_mission(
    mission_id: int,
    user: FromDishka[JwtHRUser],
    body: MissionUpdateRequest,
    use_case: FromDishka[UpdateMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission=body.to_schema(mission_id=mission_id))
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить миссию",
    description="Удаляет указанную миссию",
)
async def delete_mission(
    mission_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[DeleteMissionUseCase],
) -> None:
    _ = user
    await use_case.execute(mission_id=mission_id)


@router.post(
    path="/missions/{mission_id}/tasks/{task_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить задачу к миссии",
    description="Назначает задачу указанной миссии",
)
async def add_task_to_mission(
    mission_id: int,
    task_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddTaskToMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/tasks/{task_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить задачу из миссии",
    description="Убирает задачу из указанной миссии",
)
async def remove_task_from_mission(
    mission_id: int,
    task_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveTaskFromMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить награду компетенции к миссии",
    description="Назначает награду в виде повышения компетенции за выполнение миссии",
)
async def add_competency_reward_to_mission(
    mission_id: int,
    competency_id: int,
    body: CompetencyRewardAddRequest,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddCompetencyRewardToMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(
        mission_id=mission_id,
        competency_id=competency_id,
        level_increase=body.level_increase,
    )
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить награду компетенции из миссии",
    description="Убирает награду в виде повышения компетенции из миссии",
)
async def remove_competency_reward_from_mission(
    mission_id: int,
    competency_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveCompetencyRewardFromMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, competency_id=competency_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить награду навыка к миссии",
    description="Назначает награду в виде повышения навыка за выполнение миссии",
)
async def add_skill_reward_to_mission(
    mission_id: int,
    skill_id: int,
    body: SkillRewardAddRequest,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddSkillRewardToMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(
        mission_id=mission_id,
        skill_id=skill_id,
        level_increase=body.level_increase,
    )
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить награду навыка из миссии",
    description="Убирает награду в виде повышения навыка из миссии",
)
async def remove_skill_reward_from_mission(
    mission_id: int,
    skill_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveSkillRewardFromMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, skill_id=skill_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить артефакт к миссии",
    description="Назначает артефакт как награду за выполнение миссии",
)
async def add_artifact_to_mission(
    mission_id: int,
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddArtifactToMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить артефакт из миссии",
    description="Убирает артефакт из наград миссии",
)
async def remove_artifact_from_mission(
    mission_id: int,
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveArtifactFromMissionUseCase],
) -> MissionResponse:
    _ = user
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)
