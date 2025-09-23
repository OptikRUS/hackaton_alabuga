from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.missions.schemas import (
    MissionBranchCreateRequest,
    MissionBranchesResponse,
    MissionBranchResponse,
    MissionBranchUpdateRequest,
    MissionCreateRequest,
    MissionResponse,
    MissionsResponse,
    MissionUpdateRequest,
)
from src.core.artifacts.use_cases import (
    AddArtifactToMissionUseCase,
    RemoveArtifactFromMissionUseCase,
)
from src.core.missions.use_cases import (
    AddCompetencyRewardToMissionUseCase,
    AddSkillRewardToMissionUseCase,
    AddTaskToMissionUseCase,
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveCompetencyRewardFromMissionUseCase,
    RemoveSkillRewardFromMissionUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)

router = APIRouter(tags=["missions"], route_class=DishkaRoute)


@router.post(
    path="/missions/branches",
    status_code=status.HTTP_201_CREATED,
    summary="Создать ветку миссий",
    description="Создает новую ветку миссий в системе",
)
async def create_mission_branch(
    body: MissionBranchCreateRequest,
    use_case: FromDishka[CreateMissionBranchUseCase],
) -> MissionBranchResponse:
    branch = await use_case.execute(branch=body.to_schema())
    return MissionBranchResponse.from_schema(branch=branch)


@router.get(
    path="/missions/branches",
    status_code=status.HTTP_200_OK,
    summary="Получить список веток миссий",
    description="Возвращает все доступные ветки миссий",
)
async def get_mission_branches(
    use_case: FromDishka[GetMissionBranchesUseCase],
) -> MissionBranchesResponse:
    branches = await use_case.execute()
    return MissionBranchesResponse.from_schema(branches=branches)


@router.put(
    path="/missions/branches/{branch_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить ветку миссий",
    description="Обновляет данные указанной ветки миссий",
)
async def update_mission_branch(
    branch_id: int,
    body: MissionBranchUpdateRequest,
    use_case: FromDishka[UpdateMissionBranchUseCase],
) -> MissionBranchResponse:
    branch = await use_case.execute(branch=body.to_schema(branch_id=branch_id))
    return MissionBranchResponse.from_schema(branch=branch)


@router.delete(
    path="/missions/branches/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ветку миссий",
    description="Удаляет указанную ветку миссий",
)
async def delete_mission_branch(
    branch_id: int,
    use_case: FromDishka[DeleteMissionBranchUseCase],
) -> None:
    await use_case.execute(branch_id=branch_id)


@router.post(
    path="/missions",
    status_code=status.HTTP_201_CREATED,
    summary="Создать миссию",
    description="Создает новую миссию в системе",
)
async def create_mission(
    body: MissionCreateRequest,
    use_case: FromDishka[CreateMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission=body.to_schema())
    return MissionResponse.from_schema(mission=mission)


@router.get(
    path="/missions",
    status_code=status.HTTP_200_OK,
    summary="Получить список миссий",
    description="Возвращает все доступные миссии",
)
async def get_missions(
    use_case: FromDishka[GetMissionsUseCase],
) -> MissionsResponse:
    missions = await use_case.execute()
    return MissionsResponse.from_schema(missions=missions)


@router.get(
    path="/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить миссию по ID",
    description="Возвращает детальную информацию о миссии",
)
async def get_mission(
    mission_id: int,
    use_case: FromDishka[GetMissionDetailUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id)
    return MissionResponse.from_schema(mission=mission)


@router.put(
    path="/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить миссию",
    description="Обновляет данные указанной миссии",
)
async def update_mission(
    mission_id: int,
    body: MissionUpdateRequest,
    use_case: FromDishka[UpdateMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission=body.to_schema(mission_id=mission_id))
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить миссию",
    description="Удаляет указанную миссию",
)
async def delete_mission(
    mission_id: int,
    use_case: FromDishka[DeleteMissionUseCase],
) -> None:
    await use_case.execute(mission_id=mission_id)


@router.post(
    path="/missions/{mission_id}/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить задачу к миссии",
    description="Назначает задачу указанной миссии",
)
async def add_task_to_mission(
    mission_id: int,
    task_id: int,
    use_case: FromDishka[AddTaskToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить задачу из миссии",
    description="Убирает задачу из указанной миссии",
)
async def remove_task_from_mission(
    mission_id: int,
    task_id: int,
    use_case: FromDishka[RemoveTaskFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/competencies/{competency_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить награду компетенции к миссии",
    description="Назначает награду в виде повышения компетенции за выполнение миссии",
)
async def add_competency_reward_to_mission(
    mission_id: int,
    competency_id: int,
    level_increase: int,
    use_case: FromDishka[AddCompetencyRewardToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(
        mission_id=mission_id, competency_id=competency_id, level_increase=level_increase
    )
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/competencies/{competency_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить награду компетенции из миссии",
    description="Убирает награду в виде повышения компетенции из миссии",
)
async def remove_competency_reward_from_mission(
    mission_id: int,
    competency_id: int,
    use_case: FromDishka[RemoveCompetencyRewardFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, competency_id=competency_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить награду навыка к миссии",
    description="Назначает награду в виде повышения навыка за выполнение миссии",
)
async def add_skill_reward_to_mission(
    mission_id: int,
    skill_id: int,
    level_increase: int,
    use_case: FromDishka[AddSkillRewardToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(
        mission_id=mission_id, skill_id=skill_id, level_increase=level_increase
    )
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить награду навыка из миссии",
    description="Убирает награду в виде повышения навыка из миссии",
)
async def remove_skill_reward_from_mission(
    mission_id: int,
    skill_id: int,
    use_case: FromDishka[RemoveSkillRewardFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, skill_id=skill_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(
    path="/missions/{mission_id}/artifacts/{artifact_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить артефакт к миссии",
    description="Назначает артефакт как награду за выполнение миссии",
)
async def add_artifact_to_mission(
    mission_id: int,
    artifact_id: int,
    use_case: FromDishka[AddArtifactToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/artifacts/{artifact_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить артефакт из миссии",
    description="Убирает артефакт из наград миссии",
)
async def remove_artifact_from_mission(
    mission_id: int,
    artifact_id: int,
    use_case: FromDishka[RemoveArtifactFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)
