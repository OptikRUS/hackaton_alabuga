import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import RemoveTaskFromMissionUseCase
from src.core.tasks.exceptions import TaskNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestRemoveTaskFromMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = RemoveTaskFromMissionUseCase(storage=self.storage)
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
                title="TEST1",
                description="TEST1",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="TEST2",
                description="TEST2",
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)

    async def test_execute_success(self):
        mission = await self.use_case.execute(mission_id=1, task_id=1)

        assert mission == self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=2,
                    title="TEST2",
                    description="TEST2",
                )
            ],
        )

    async def test_execute_mission_not_found(self):
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999, task_id=1)

    async def test_execute_task_not_found(self):
        with pytest.raises(TaskNotFoundError):
            await self.use_case.execute(mission_id=1, task_id=999)
