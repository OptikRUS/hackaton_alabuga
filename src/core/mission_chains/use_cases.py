from dataclasses import dataclass

from src.core.mission_chains.exceptions import (
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
)
from src.core.mission_chains.schemas import MissionChain, MissionChains
from src.core.missions.exceptions import MissionNotFoundError, PrerequisiteMissionNotFoundError
from src.core.storages import MissionStorage
from src.core.use_case import UseCase


@dataclass
class CreateMissionChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_chain: MissionChain) -> MissionChain:
        try:
            await self.storage.get_mission_chain_by_name(name=mission_chain.name)
            raise MissionChainNameAlreadyExistError
        except MissionChainNotFoundError:
            await self.storage.insert_mission_chain(mission_chain=mission_chain)
            return await self.storage.get_mission_chain_by_name(name=mission_chain.name)


@dataclass
class GetMissionChainsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> MissionChains:
        return await self.storage.list_mission_chains()


@dataclass
class GetMissionChainDetailUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, chain_id: int) -> MissionChain:
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)


@dataclass
class UpdateMissionChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_chain: MissionChain) -> MissionChain:
        try:
            await self.storage.get_mission_chain_by_name(name=mission_chain.name)
            raise MissionChainNameAlreadyExistError
        except MissionChainNotFoundError:
            await self.storage.update_mission_chain(mission_chain=mission_chain)
            return await self.storage.get_mission_chain_by_id(chain_id=mission_chain.id)


@dataclass
class DeleteMissionChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, chain_id: int) -> None:
        await self.storage.delete_mission_chain(chain_id=chain_id)


@dataclass
class AddMissionToChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, chain_id: int, mission_id: int) -> MissionChain:
        await self.storage.get_mission_chain_by_id(chain_id=chain_id)
        await self.storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.add_mission_to_chain(chain_id=chain_id, mission_id=mission_id)
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)


@dataclass
class RemoveMissionFromChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, chain_id: int, mission_id: int) -> MissionChain:
        await self.storage.remove_mission_from_chain(chain_id=chain_id, mission_id=mission_id)
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)


@dataclass
class AddMissionDependencyUseCase(UseCase):
    storage: MissionStorage

    async def execute(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> MissionChain:
        await self.storage.get_mission_chain_by_id(chain_id=chain_id)

        # Check mission_id first
        try:
            await self.storage.get_mission_by_id(mission_id=mission_id)
        except MissionNotFoundError as err:
            raise MissionNotFoundError from err

        # Check prerequisite_mission_id
        try:
            await self.storage.get_mission_by_id(mission_id=prerequisite_mission_id)
        except MissionNotFoundError as err:
            raise PrerequisiteMissionNotFoundError from err

        await self.storage.add_mission_dependency(
            chain_id=chain_id,
            mission_id=mission_id,
            prerequisite_mission_id=prerequisite_mission_id,
        )
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)


@dataclass
class RemoveMissionDependencyUseCase(UseCase):
    storage: MissionStorage

    async def execute(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> MissionChain:
        await self.storage.remove_mission_dependency(
            chain_id=chain_id,
            mission_id=mission_id,
            prerequisite_mission_id=prerequisite_mission_id,
        )
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)
