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
    AddTaskToMissionUseCase,
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)

router = APIRouter(tags=["missions"], route_class=DishkaRoute)


@router.post(path="/missions/branches", status_code=status.HTTP_201_CREATED)
async def create_mission_branch(
    body: MissionBranchCreateRequest,
    use_case: FromDishka[CreateMissionBranchUseCase],
) -> MissionBranchResponse:
    branch = await use_case.execute(branch=body.to_schema())
    return MissionBranchResponse.from_schema(branch=branch)


@router.get(path="/missions/branches", status_code=status.HTTP_200_OK)
async def get_mission_branches(
    use_case: FromDishka[GetMissionBranchesUseCase],
) -> MissionBranchesResponse:
    branches = await use_case.execute()
    return MissionBranchesResponse.from_schema(branches=branches)


@router.put(path="/missions/branches/{branch_id}", status_code=status.HTTP_200_OK)
async def update_mission_branch(
    branch_id: int,
    body: MissionBranchUpdateRequest,
    use_case: FromDishka[UpdateMissionBranchUseCase],
) -> MissionBranchResponse:
    branch = await use_case.execute(branch=body.to_schema(branch_id=branch_id))
    return MissionBranchResponse.from_schema(branch=branch)


@router.delete(path="/missions/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission_branch(
    branch_id: int,
    use_case: FromDishka[DeleteMissionBranchUseCase],
) -> None:
    await use_case.execute(branch_id=branch_id)


@router.post(path="/missions", status_code=status.HTTP_201_CREATED)
async def create_mission(
    body: MissionCreateRequest,
    use_case: FromDishka[CreateMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission=body.to_schema())
    return MissionResponse.from_schema(mission=mission)


@router.get(path="/missions", status_code=status.HTTP_200_OK)
async def get_missions(
    use_case: FromDishka[GetMissionsUseCase],
) -> MissionsResponse:
    missions = await use_case.execute()
    return MissionsResponse.from_schema(missions=missions)


@router.get(path="/missions/{mission_id}", status_code=status.HTTP_200_OK)
async def get_mission(
    mission_id: int,
    use_case: FromDishka[GetMissionDetailUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id)
    return MissionResponse.from_schema(mission=mission)


@router.put(path="/missions/{mission_id}", status_code=status.HTTP_200_OK)
async def update_mission(
    mission_id: int,
    body: MissionUpdateRequest,
    use_case: FromDishka[UpdateMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission=body.to_schema(mission_id=mission_id))
    return MissionResponse.from_schema(mission=mission)


@router.delete(path="/missions/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission(
    mission_id: int,
    use_case: FromDishka[DeleteMissionUseCase],
) -> None:
    await use_case.execute(mission_id=mission_id)


@router.post(path="/missions/{mission_id}/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def add_task_to_mission(
    mission_id: int,
    task_id: int,
    use_case: FromDishka[AddTaskToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(path="/missions/{mission_id}/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def remove_task_from_mission(
    mission_id: int,
    task_id: int,
    use_case: FromDishka[RemoveTaskFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, task_id=task_id)
    return MissionResponse.from_schema(mission=mission)


@router.post(path="/missions/{mission_id}/artifacts/{artifact_id}", status_code=status.HTTP_200_OK)
async def add_artifact_to_mission(
    mission_id: int,
    artifact_id: int,
    use_case: FromDishka[AddArtifactToMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)


@router.delete(
    path="/missions/{mission_id}/artifacts/{artifact_id}", status_code=status.HTTP_200_OK
)
async def remove_artifact_from_mission(
    mission_id: int,
    artifact_id: int,
    use_case: FromDishka[RemoveArtifactFromMissionUseCase],
) -> MissionResponse:
    mission = await use_case.execute(mission_id=mission_id, artifact_id=artifact_id)
    return MissionResponse.from_schema(mission=mission)
