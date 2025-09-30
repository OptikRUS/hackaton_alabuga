import pytest

from src.core.missions.exceptions import MissionNotCompletedError
from src.core.missions.use_cases import ApproveUserMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestApproveUserMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = ApproveUserMissionUseCase(
            mission_storage=self.storage,
            artifact_storage=self.storage,
            user_storage=self.storage,
            competency_storage=self.storage,
        )

    async def test_approve_completed_mission_rewards_user(self) -> None:
        await self.storage.insert_user(
            user=self.factory.candidate(login="test_user", exp=100, mana=50)
        )

        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="Task 1",
                description="First task",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="Task 2",
                description="Second task",
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=200,
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(
                        task_id=1,
                        title="Task 1",
                        description="First task",
                    ),
                    self.factory.mission_task(
                        task_id=2,
                        title="Task 2",
                        description="Second task",
                    ),
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")
        await self.storage.update_user_task_completion(task_id=2, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 300  # 100 + 200
        assert updated_user.mana == 150  # 50 + 100

    async def test_approve_incomplete_mission_raises_error(self) -> None:
        await self.storage.insert_user(
            user=self.factory.candidate(login="test_user", exp=100, mana=50)
        )

        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="Task 1",
                description="First task",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="Task 2",
                description="Second task",
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=200,
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(
                        task_id=1,
                        title="Task 1",
                        description="First task",
                    ),
                    self.factory.mission_task(
                        task_id=2,
                        title="Task 2",
                        description="Second task",
                    ),
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        # Помечаем только одну задачу как выполненную
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        with pytest.raises(MissionNotCompletedError):
            await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что награды не начислены
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 100  # без изменений
        assert updated_user.mana == 50  # без изменений
