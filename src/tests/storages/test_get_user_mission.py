import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.users.enums import UserRoleEnum
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestGetUserMission(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_user(
            user=self.factory.user(login="TEST", role=UserRoleEnum.CANDIDATE)
        )
        season_model = await self.storage_helper.insert_season(
            season=self.factory.season(season_id=1, name="Test Season")
        )
        assert season_model is not None
        season = season_model.to_schema()

        mission_model = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=season.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert mission_model is not None
        self.mission = mission_model.to_schema()

    async def test_get_user_mission_no_tasks(self) -> None:
        user_mission = await self.storage.get_user_mission(
            mission_id=self.mission.id,
            user_login="TEST",
        )

        assert user_mission == self.factory.user_mission(
            mission_id=self.mission.id,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.mission.season_id,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
            user_tasks=[],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_user_mission_with_tasks_no_user_assignments(self) -> None:
        task1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="Description 1")
        )
        task2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=2, title="Task 2", description="Description 2")
        )
        assert task1 is not None
        assert task2 is not None

        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task1.id,
        )
        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task2.id,
        )

        user_mission = await self.storage.get_user_mission(
            mission_id=self.mission.id,
            user_login="TEST",
        )

        assert user_mission == self.factory.user_mission(
            mission_id=self.mission.id,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.mission.season_id,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=task1.id, title="Task 1", description="Description 1"
                ),
                self.factory.mission_task(
                    task_id=task2.id, title="Task 2", description="Description 2"
                ),
            ],
            user_tasks=[
                self.factory.user_task(
                    task_id=task1.id,
                    title="Task 1",
                    description="Description 1",
                    is_completed=False,
                ),
                self.factory.user_task(
                    task_id=task2.id,
                    title="Task 2",
                    description="Description 2",
                    is_completed=False,
                ),
            ],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_user_mission_with_partial_user_assignments(self) -> None:
        task1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="Description 1")
        )
        task2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=2, title="Task 2", description="Description 2")
        )
        task3 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=3, title="Task 3", description="Description 3")
        )
        assert task1 is not None
        assert task2 is not None
        assert task3 is not None

        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task1.id,
        )
        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task2.id,
        )
        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task3.id,
        )

        await self.storage_helper.insert_user_task_relation(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=task1.id,
                title="Task 1",
                description="Description 1",
                is_completed=True,
            ),
        )
        await self.storage_helper.insert_user_task_relation(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=task2.id,
                title="Task 2",
                description="Description 2",
                is_completed=False,
            ),
        )

        user_mission = await self.storage.get_user_mission(
            mission_id=self.mission.id,
            user_login="TEST",
        )

        assert user_mission == self.factory.user_mission(
            mission_id=self.mission.id,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.mission.season_id,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=task1.id, title="Task 1", description="Description 1"
                ),
                self.factory.mission_task(
                    task_id=task2.id, title="Task 2", description="Description 2"
                ),
                self.factory.mission_task(
                    task_id=task3.id, title="Task 3", description="Description 3"
                ),
            ],
            user_tasks=[
                self.factory.user_task(
                    task_id=task1.id, title="Task 1", description="Description 1", is_completed=True
                ),
                self.factory.user_task(
                    task_id=task2.id,
                    title="Task 2",
                    description="Description 2",
                    is_completed=False,
                ),
                self.factory.user_task(
                    task_id=task3.id,
                    title="Task 3",
                    description="Description 3",
                    is_completed=False,
                ),
            ],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_user_mission_all_tasks_completed(self) -> None:
        task1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="Description 1")
        )
        task2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(task_id=2, title="Task 2", description="Description 2")
        )
        assert task1 is not None
        assert task2 is not None

        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task1.id,
        )
        await self.storage_helper.insert_mission_task_relation(
            mission_id=self.mission.id,
            task_id=task2.id,
        )

        await self.storage_helper.insert_user_task_relation(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=task1.id,
                title="Task 1",
                description="Description 1",
                is_completed=True,
            ),
        )
        await self.storage_helper.insert_user_task_relation(
            user_login="TEST",
            user_task=self.factory.user_task(
                task_id=task2.id,
                title="Task 2",
                description="Description 2",
                is_completed=True,
            ),
        )

        user_mission = await self.storage.get_user_mission(
            mission_id=self.mission.id,
            user_login="TEST",
        )

        expected_user_mission = self.factory.user_mission(
            mission_id=self.mission.id,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.mission.season_id,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=task1.id, title="Task 1", description="Description 1"
                ),
                self.factory.mission_task(
                    task_id=task2.id, title="Task 2", description="Description 2"
                ),
            ],
            user_tasks=[
                self.factory.user_task(
                    task_id=task1.id, title="Task 1", description="Description 1", is_completed=True
                ),
                self.factory.user_task(
                    task_id=task2.id, title="Task 2", description="Description 2", is_completed=True
                ),
            ],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )
        assert user_mission == expected_user_mission

    async def test_get_user_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_user_mission(mission_id=999, user_login="NONEXISTENT_USER")
