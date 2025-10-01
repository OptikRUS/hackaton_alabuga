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
        self.use_case = AddTaskToMissionUseCase(storage=self.storage, user_storage=self.storage)
        await self.storage.insert_season(
            season=self.factory.season(season_id=1, name="TEST_SEASON")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="TEST_MISSION",
                description="Test mission description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="TEST_TASK",
                description="Test task description",
            )
        )

    async def test_execute_success_with_users_assignment(self):
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="user1",
                first_name="John",
                last_name="Doe",
                rank_id=1,
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="user2",
                first_name="Jane",
                last_name="Smith",
                rank_id=1,
            )
        )

        result = await self.use_case.execute(mission_id=1, task_id=1)

        assert result.tasks is not None
        assert len(result.tasks) == 1
        assert result.tasks[0].id == 1
        assert result.tasks[0].title == "TEST_TASK"
        assert result.tasks[0].description == "Test task description"
        user1_tasks = await self.storage.get_user_tasks(user_login="user1")
        user2_tasks = await self.storage.get_user_tasks(user_login="user2")
        assert len(user1_tasks) == 1
        assert user1_tasks[0].id == 1
        assert user1_tasks[0].title == "TEST_TASK"
        assert user1_tasks[0].description == "Test task description"
        assert user1_tasks[0].is_completed is False
        assert len(user2_tasks) == 1
        assert user2_tasks[0].id == 1
        assert user2_tasks[0].title == "TEST_TASK"
        assert user2_tasks[0].description == "Test task description"
        assert user2_tasks[0].is_completed is False

    async def test_execute_success_without_users(self):
        result = await self.use_case.execute(mission_id=1, task_id=1)

        assert result.tasks is not None
        assert len(result.tasks) == 1
        assert result.tasks[0].id == 1
        assert result.tasks[0].title == "TEST_TASK"

    async def test_execute_success_with_different_rank_users(self):
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="user_different",
                first_name="Bob",
                last_name="Johnson",
                rank_id=2,  # Другой ранг
            )
        )

        result = await self.use_case.execute(mission_id=1, task_id=1)

        assert result.tasks is not None
        assert len(result.tasks) == 1
        user_tasks = await self.storage.get_user_tasks(user_login="user_different")
        assert len(user_tasks) == 0

    async def test_execute_mission_not_found(self):
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999, task_id=1)

    async def test_execute_task_not_found(self):
        with pytest.raises(TaskNotFoundError):
            await self.use_case.execute(mission_id=1, task_id=999)

    async def test_execute_multiple_tasks_assignment(self):
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="TEST_TASK_2",
                description="Test task 2 description",
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="user_multiple",
                first_name="Alice",
                last_name="Brown",
                rank_id=1,
            )
        )

        await self.use_case.execute(mission_id=1, task_id=1)
        result = await self.use_case.execute(mission_id=1, task_id=2)

        assert result.tasks is not None
        assert len(result.tasks) == 2
        task_ids = [task.id for task in result.tasks]
        assert 1 in task_ids
        assert 2 in task_ids
        user_tasks = await self.storage.get_user_tasks(user_login="user_multiple")
        assert len(user_tasks) == 2
        user_task_ids = [task.id for task in user_tasks]
        assert 1 in user_task_ids
        assert 2 in user_task_ids

    async def test_execute_with_multiple_ranks(self):
        user_rank_1 = self.factory.candidate(
            login="user_rank_1",
            first_name="Rank1",
            last_name="User",
            rank_id=1,
        )
        user_rank_2 = self.factory.candidate(
            login="user_rank_2",
            first_name="Rank2",
            last_name="User",
            rank_id=2,
        )
        user_rank_3 = self.factory.candidate(
            login="user_rank_3",
            first_name="Rank3",
            last_name="User",
            rank_id=3,
        )
        await self.storage.insert_user(user=user_rank_1)
        await self.storage.insert_user(user=user_rank_2)
        await self.storage.insert_user(user=user_rank_3)

        result = await self.use_case.execute(mission_id=1, task_id=1)

        assert result.tasks is not None
        assert len(result.tasks) == 1
        rank_1_tasks = await self.storage.get_user_tasks(user_login="user_rank_1")
        rank_2_tasks = await self.storage.get_user_tasks(user_login="user_rank_2")
        rank_3_tasks = await self.storage.get_user_tasks(user_login="user_rank_3")
        assert len(rank_1_tasks) == 1
        assert rank_1_tasks[0].id == 1
        assert len(rank_2_tasks) == 0
        assert len(rank_3_tasks) == 0

    async def test_execute_task_properties_preserved(self):
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="Detailed Task",
                description="!@#$%^&*()",
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="user_detailed",
                first_name="Detailed",
                last_name="User",
                rank_id=1,
            )
        )

        result = await self.use_case.execute(mission_id=1, task_id=2)

        assert result.tasks is not None
        assert len(result.tasks) == 1
        assert result.tasks[0].id == 2
        assert result.tasks[0].title == "Detailed Task"
        assert result.tasks[0].description == "!@#$%^&*()"
        user_tasks = await self.storage.get_user_tasks(user_login="user_detailed")
        assert len(user_tasks) == 1
        assert user_tasks[0].id == 2
        assert user_tasks[0].title == "Detailed Task"
        assert user_tasks[0].description == "!@#$%^&*()"
        assert user_tasks[0].is_completed is False
