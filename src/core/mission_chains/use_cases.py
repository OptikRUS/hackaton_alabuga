from dataclasses import dataclass

from src.core.mission_chains.exceptions import (
    CircularDependencyError,
    InvalidMissionOrderError,
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
        await self.storage.get_mission_chain_by_id(chain_id=mission_chain.id)
        try:
            existing_chain = await self.storage.get_mission_chain_by_name(name=mission_chain.name)
            if existing_chain.id != mission_chain.id:
                raise MissionChainNameAlreadyExistError
        except MissionChainNotFoundError:
            pass
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
class UpdateMissionOrderInChainUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, chain_id: int, mission_id: int, new_order: int) -> MissionChain:
        # Проверяем, что цепочка и миссия существуют
        mission_chain = await self.storage.get_mission_chain_by_id(chain_id=chain_id)
        await self.storage.get_mission_by_id(mission_id=mission_id)

        # Валидация порядка
        if new_order < 1:
            raise InvalidMissionOrderError

        # Получаем количество миссий в цепочке
        missions_count = len(mission_chain.missions) if mission_chain.missions else 0

        if new_order > missions_count:
            raise InvalidMissionOrderError

        await self.storage.update_mission_order_in_chain(
            chain_id=chain_id, mission_id=mission_id, new_order=new_order
        )
        return await self.storage.get_mission_chain_by_id(chain_id=chain_id)


@dataclass
class AddMissionDependencyUseCase(UseCase):
    storage: MissionStorage

    def _check_circular_dependency(
        self, dependencies: list, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        """Проверяет наличие циклических зависимостей"""
        # Проверяем, что миссия не зависит от самой себя
        if mission_id == prerequisite_mission_id:
            raise CircularDependencyError

        # Stroim граф зависимостей для проверки циклов
        dependency_graph = self._build_dependency_graph(
            dependencies, mission_id, prerequisite_mission_id
        )

        # Проверяем наличие цикла s pomoshchyu DFS
        if self._has_cycle_in_graph(dependency_graph):
            raise CircularDependencyError

    def _build_dependency_graph(
        self, dependencies: list, mission_id: int, prerequisite_mission_id: int
    ) -> dict[int, list[int]]:
        """Строит граф зависимостей"""
        dependency_graph: dict[int, list[int]] = {}
        for dep in dependencies:
            if dep.mission_id not in dependency_graph:
                dependency_graph[dep.mission_id] = []
            dependency_graph[dep.mission_id].append(dep.prerequisite_mission_id)

        # Добавляем новую зависимость для проверки
        if mission_id not in dependency_graph:
            dependency_graph[mission_id] = []
        dependency_graph[mission_id].append(prerequisite_mission_id)

        return dependency_graph

    def _has_cycle_in_graph(self, dependency_graph: dict) -> bool:
        """Проверяет наличие цикла в графе s pomoshchyu DFS"""
        visited = set()

        def has_cycle_dfs(node: int, rec_stack: set) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in dependency_graph.get(node, []):
                if (
                    neighbor not in visited and has_cycle_dfs(neighbor, rec_stack)
                ) or neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        # Проверяем все узлы на наличие циклов
        for node in dependency_graph:
            return node not in visited and has_cycle_dfs(node, set())

        return False

    async def execute(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> MissionChain:
        mission_chain = await self.storage.get_mission_chain_by_id(chain_id=chain_id)

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

        # Проверяем циклические зависимости
        existing_dependencies = mission_chain.dependencies or []
        self._check_circular_dependency(existing_dependencies, mission_id, prerequisite_mission_id)

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
