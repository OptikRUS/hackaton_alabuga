from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.missions.schemas import (
    MissionBranchCreateRequest,
    MissionBranchesResponse,
    MissionBranchResponse,
    MissionCreateRequest,
    MissionResponse,
    MissionsResponse,
    MissionUpdateRequest,
)
from src.core.missions.use_cases import (
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionsUseCase,
    GetMissionUseCase,
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
    use_case: FromDishka[GetMissionUseCase],
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
