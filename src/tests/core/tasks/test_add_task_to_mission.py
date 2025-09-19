import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import AddTaskToMissionUseCase
from src.core.tasks.exceptions import TaskNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestAddTaskToMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = AddTaskToMissionUseCase(storage=self.storage)
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="TEST",
                description="TEST",
            )
        )

    async def test_execute_success(self):
        result = await self.use_case.execute(mission_id=1, task_id=1)

        assert result == self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=1,
                    title="TEST",
                    description="TEST",
                )
            ],
        )

    async def test_execute_mission_not_found(self):
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999, task_id=1)

    async def test_execute_task_not_found(self):
        with pytest.raises(TaskNotFoundError):
            await self.use_case.execute(mission_id=1, task_id=999)
