import pytest

from src.core.mission_chains.exceptions import CircularDependencyError
from src.core.mission_chains.use_cases import AddMissionDependencyUseCase
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError, PrerequisiteMissionNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCircularDependencyUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = AddMissionDependencyUseCase(storage=self.storage)

        # Настраиваем базовые данные
        await self.storage.insert_season(season=self.factory.season(season_id=1, name="TEST"))
        await self.storage.insert_mission_chain(
            mission_chain=self.factory.mission_chain(
                chain_id=1,
                name="TEST_CHAIN",
                description="Test chain description",
                reward_xp=200,
                reward_mana=100,
            )
        )

        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="MISSION_1",
                description="First mission",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=2,
                title="MISSION_2",
                description="Second mission",
                reward_xp=150,
                reward_mana=75,
                rank_requirement=2,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=3,
                title="MISSION_3",
                description="Third mission",
                reward_xp=200,
                reward_mana=100,
                rank_requirement=3,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )

    async def test_add_mission_dependency_self_dependency_raises_error(self) -> None:
        """Тест: попытка добавить зависимость миссии от самой себя должна вызывать ошибку"""
        # Act & Assert
        with pytest.raises(CircularDependencyError):
            await self.use_case.execute(
                chain_id=1,
                mission_id=1,
                prerequisite_mission_id=1,
            )

    async def test_add_mission_dependency_circular_dependency_raises_error(self) -> None:
        """Тест: попытка создать циклическую зависимость должна вызывать ошибку"""
        # Добавляем первую зависимость: mission1 зависит от mission2
        await self.use_case.execute(
            chain_id=1,
            mission_id=1,
            prerequisite_mission_id=2,
        )

        # Act & Assert
        # Попытка добавить обратную зависимость: mission2 зависит от mission1
        # должна вызвать ошибку циклической зависимости
        with pytest.raises(CircularDependencyError):
            await self.use_case.execute(
                chain_id=1,
                mission_id=2,
                prerequisite_mission_id=1,
            )

    async def test_add_mission_dependency_complex_circular_dependency_raises_error(self) -> None:
        """Тест: попытка создать сложную циклическую зависимость должна вызывать ошибку"""
        # Создаем цепочку зависимостей: mission1 -> mission2 -> mission3
        await self.use_case.execute(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )
        await self.use_case.execute(
            chain_id=1,
            mission_id=3,
            prerequisite_mission_id=2,
        )

        # Act & Assert
        # Попытка замкнуть цикл: mission1 зависит от mission3
        # должна вызвать ошибку циклической зависимости
        with pytest.raises(CircularDependencyError):
            await self.use_case.execute(
                chain_id=1,
                mission_id=1,
                prerequisite_mission_id=3,
            )

    async def test_add_mission_dependency_valid_dependency_succeeds(self) -> None:
        """Тест: добавление валидной зависимости должно проходить успешно"""
        # Act
        result = await self.use_case.execute(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        # Assert
        assert result is not None
        assert result.dependencies is not None
        assert len(result.dependencies) == 1
        assert result.dependencies[0].mission_id == 2
        assert result.dependencies[0].prerequisite_mission_id == 1

    async def test_add_mission_dependency_mission_not_found_raises_error(self) -> None:
        """Тест: попытка добавить зависимость для несуществующей миссии должна вызывать ошибку"""
        # Act & Assert
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(
                chain_id=1,
                mission_id=999,  # Несуществующий ID
                prerequisite_mission_id=1,
            )

    async def test_add_mission_dependency_prerequisite_mission_not_found_raises_error(self) -> None:
        """Тест: попытка добавить зависимость от несуществующей миссии должна вызывать ошибку"""
        # Act & Assert
        with pytest.raises(PrerequisiteMissionNotFoundError):
            await self.use_case.execute(
                chain_id=1,
                mission_id=1,
                prerequisite_mission_id=999,  # Несуществующий ID
            )
