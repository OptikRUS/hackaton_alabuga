import pytest

from src.core.tasks.use_cases import TaskApproveUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestTaskApproveUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = TaskApproveUseCase(storage=self.storage)

    async def test_approve_task_when_last_task_completed_no_rewards(self) -> None:
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

        await self.use_case.execute(
            params=self.factory.task_approve_params(task_id=2, user_login="test_user")
        )

        updated_user = await self.storage.get_user_by_login("test_user")
        assert (
            updated_user.exp == 100
        )  # без изменений - награды теперь начисляются при одобрении миссии
        assert (
            updated_user.mana == 50
        )  # без изменений - награды теперь начисляются при одобрении миссии

    async def test_approve_task_when_not_last_task_no_rewards(self) -> None:
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                exp=100,
                mana=50,
            )
        )

        await self.storage.insert_mission_task(
            self.factory.mission_task(
                task_id=1,
                title="Task 1",
                description="First task",
            )
        )
        await self.storage.insert_mission_task(
            self.factory.mission_task(
                task_id=2,
                title="Task 2",
                description="Second task",
            )
        )
        await self.storage.insert_mission_task(
            self.factory.mission_task(
                task_id=3,
                title="Task 3",
                description="Third task",
            )
        )

        await self.storage.insert_mission(
            self.factory.mission(
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
                    self.factory.mission_task(
                        task_id=3,
                        title="Task 3",
                        description="Third task",
                    ),
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        await self.storage.add_task_to_mission(mission_id=1, task_id=3)

        await self.storage.update_user_task_completion(1, "test_user")

        await self.use_case.execute(
            params=self.factory.task_approve_params(task_id=2, user_login="test_user")
        )

        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 100  # без изменений
        assert updated_user.mana == 50  # без изменений
