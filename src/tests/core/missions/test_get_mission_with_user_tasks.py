import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import GetMissionWithUserTasksUseCase
from src.core.users.enums import UserRoleEnum
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionWithUserTasksUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionWithUserTasksUseCase(storage=self.storage)

    async def test_get_mission_with_user_tasks_empty(self) -> None:
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )

        user_mission = await self.use_case.execute(mission_id=1, user_login="TEST")

        # TODO: по хорошему написать фабрику на user_mission и сравнивать
        assert user_mission.id == 1
        assert user_mission.title == "Test Mission"
        assert user_mission.description == "Test Description"
        assert user_mission.reward_xp == 100
        assert user_mission.reward_mana == 50
        assert user_mission.rank_requirement == 1
        assert user_mission.category == MissionCategoryEnum.QUEST
        assert user_mission.user_tasks == []
        assert not user_mission.is_completed

    async def test_get_mission_with_user_tasks_with_completed_tasks(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(login="TEST", role=UserRoleEnum.CANDIDATE)
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="Description 1")
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=2, title="Task 2", description="Description 2")
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        await self.storage.add_user_task(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=1,
                title="Task 1",
                description="Description 1",
                is_completed=True,
            ),
        )
        await self.storage.add_user_task(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=2,
                title="Task 2",
                description="Description 2",
                is_completed=False,
            ),
        )

        user_mission = await self.use_case.execute(mission_id=1, user_login="TEST")

        # TODO: по хорошему написать фабрику на user_mission и сравнивать
        assert user_mission.id == 1
        assert user_mission.title == "Test Mission"
        assert user_mission.user_tasks is not None
        assert len(user_mission.user_tasks) == 2
        assert user_mission.user_tasks[0].title == "Task 1"
        assert user_mission.user_tasks[0].is_completed is True
        assert user_mission.user_tasks[1].title == "Task 2"
        assert user_mission.user_tasks[1].is_completed is False
        assert not user_mission.is_completed

    async def test_get_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999, user_login="123")
