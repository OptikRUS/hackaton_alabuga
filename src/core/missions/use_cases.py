from dataclasses import dataclass

from src.core.missions.exceptions import (
    MissionAlreadyExistError,
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNotFoundError,
)
from src.core.missions.schemas import Mission, MissionBranch, MissionBranches, Missions
from src.core.storages import MissionBranchStorage, MissionStorage
from src.core.use_case import UseCase


@dataclass
class CreateMissionBranchUseCase(UseCase):
    storage: MissionBranchStorage

    async def execute(self, branch: MissionBranch) -> MissionBranch:
        try:
            await self.storage.get_mission_branch_by_name(name=branch.name)
            raise MissionBranchAlreadyExistError
        except MissionBranchNotFoundError:
            await self.storage.insert_mission_branch(branch=branch)
            return await self.storage.get_mission_branch_by_name(name=branch.name)


@dataclass
class GetMissionBranchesUseCase(UseCase):
    storage: MissionBranchStorage

    async def execute(self) -> MissionBranches:
        return await self.storage.list_mission_branches()


@dataclass
class CreateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionAlreadyExistError
        except MissionNotFoundError:
            await self.storage.insert_mission(mission=mission)
            return await self.storage.get_mission_by_title(title=mission.title)


@dataclass
class GetMissionsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> Missions:
        return await self.storage.list_missions()


@dataclass
class GetMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> Mission:
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class UpdateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionAlreadyExistError
        except MissionNotFoundError:
            await self.storage.update_mission(mission=mission)
            return await self.storage.get_mission_by_id(mission_id=mission.id)


@dataclass
class DeleteMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> None:
        await self.storage.delete_mission(mission_id=mission_id)
