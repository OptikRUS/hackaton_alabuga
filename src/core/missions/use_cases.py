from dataclasses import dataclass

from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
)
from src.core.missions.schemas import (
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
)
from src.core.storages import MissionStorage
from src.core.use_case import UseCase


@dataclass
class CreateMissionBranchUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch: MissionBranch) -> MissionBranch:
        try:
            await self.storage.get_mission_branch_by_name(name=branch.name)
            raise MissionBranchNameAlreadyExistError
        except MissionBranchNotFoundError:
            await self.storage.insert_mission_branch(branch=branch)
            return await self.storage.get_mission_branch_by_name(name=branch.name)


@dataclass
class GetMissionBranchesUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> MissionBranches:
        return await self.storage.list_mission_branches()


@dataclass
class CreateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        await self.storage.get_mission_branch_by_id(branch_id=mission.branch_id)
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionNameAlreadyExistError
        except MissionNotFoundError:
            await self.storage.insert_mission(mission=mission)
            return await self.storage.get_mission_by_title(title=mission.title)


@dataclass
class GetMissionsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> Missions:
        return await self.storage.list_missions()


@dataclass
class GetMissionDetailUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> Mission:
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class UpdateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        await self.storage.get_mission_branch_by_id(branch_id=mission.branch_id)
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionNameAlreadyExistError
        except MissionNotFoundError:
            await self.storage.update_mission(mission=mission)
            return await self.storage.get_mission_by_id(mission_id=mission.id)


@dataclass
class DeleteMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> None:
        await self.storage.delete_mission(mission_id=mission_id)


@dataclass
class UpdateMissionBranchUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch: MissionBranch) -> MissionBranch:
        await self.storage.get_mission_branch_by_id(branch_id=branch.id)
        try:
            existing_branch = await self.storage.get_mission_branch_by_name(name=branch.name)
            if existing_branch.id != branch.id:
                raise MissionBranchNameAlreadyExistError
        except MissionBranchNotFoundError:
            pass
        await self.storage.update_mission_branch(branch=branch)
        return await self.storage.get_mission_branch_by_id(branch_id=branch.id)


@dataclass
class DeleteMissionBranchUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch_id: int) -> None:
        await self.storage.delete_mission_branch(branch_id=branch_id)


@dataclass
class AddTaskToMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, task_id: int) -> Mission:
        await self.storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_mission_task_by_id(task_id=task_id)
        await self.storage.add_task_to_mission(mission_id=mission_id, task_id=task_id)
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class RemoveTaskFromMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, task_id: int) -> Mission:
        await self.storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_mission_task_by_id(task_id=task_id)
        await self.storage.remove_task_from_mission(mission_id=mission_id, task_id=task_id)
        return await self.storage.get_mission_by_id(mission_id=mission_id)
