from dataclasses import dataclass

from src.core.missions.exceptions import (
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
)
from src.core.missions.schemas import MissionBranch, MissionBranches
from src.core.storages import MissionBranchStorage
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
