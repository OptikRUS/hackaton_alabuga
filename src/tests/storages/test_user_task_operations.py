import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.tasks.exceptions import TaskNotFoundError
from src.core.users.enums import UserRoleEnum
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestUserTaskOperations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="test_user",
                password="password",
                first_name="Test",
                last_name="User",
                role=UserRoleEnum.CANDIDATE,
            )
        )
        await self.storage_helper.insert_season(season=self.factory.season(name="Test Season"))
        inserted_branch = await self.storage_helper.get_branch_by_name(name="Test Season")
        assert inserted_branch is not None
        self.created_branch = inserted_branch.to_schema()
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Test Mission",
                description="Test description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert inserted_mission is not None
        self.created_mission = inserted_mission.to_schema()
        inserted_task = await self.storage_helper.insert_task(
            task=self.factory.mission_task(
                title="Test Task",
                description="Test task description",
            )
        )
        assert inserted_task is not None
        self.created_task = inserted_task.to_schema()

        await self.storage.add_task_to_mission(
            mission_id=self.created_mission.id,
            task_id=self.created_task.id,
        )
        await self.storage.add_user_task(
            user_login="test_user",
            user_task=self.factory.user_task(
                task_id=self.created_task.id,
                title=self.created_task.title,
                description=self.created_task.description,
                is_completed=False,
            ),
        )

    async def test_update_user_task_completion(self) -> None:
        user_mission = await self.storage.get_user_mission(
            mission_id=self.created_mission.id,
            user_login="test_user",
        )
        user_task = next(
            task for task in user_mission.user_tasks if task.id == self.created_task.id
        )
        assert not user_task.is_completed

        await self.storage.update_user_task_completion(
            task_id=self.created_task.id,
            user_login="test_user",
        )

        user_mission = await self.storage.get_user_mission(
            mission_id=self.created_mission.id,
            user_login="test_user",
        )
        user_task = next(
            task for task in user_mission.user_tasks if task.id == self.created_task.id
        )
        assert user_task.is_completed

    async def test_update_user_exp_and_mana(self) -> None:
        user_before = await self.storage.get_user_by_login(login="test_user")
        initial_exp = user_before.exp
        initial_mana = user_before.mana

        await self.storage.update_user_exp_and_mana(
            user_login="test_user",
            exp_increase=50,
            mana_increase=25,
        )

        user_after = await self.storage.get_user_by_login(login="test_user")
        assert user_after.exp == initial_exp + 50
        assert user_after.mana == initial_mana + 25

    async def test_update_user_exp_and_mana_negative_values(self) -> None:
        user_before = await self.storage.get_user_by_login(login="test_user")
        initial_exp = user_before.exp
        initial_mana = user_before.mana

        await self.storage.update_user_exp_and_mana(
            user_login="test_user",
            exp_increase=0,
            mana_increase=-10,
        )

        user_after = await self.storage.get_user_by_login(login="test_user")
        assert user_after.exp == initial_exp + 0
        assert user_after.mana == initial_mana - 10

    async def test_get_mission_by_task(self) -> None:
        mission = await self.storage.get_mission_by_task(task_id=self.created_task.id)

        assert mission.id == self.created_mission.id
        assert mission.title == self.created_mission.title
        assert mission.description == self.created_mission.description
        assert mission.reward_xp == self.created_mission.reward_xp
        assert mission.reward_mana == self.created_mission.reward_mana
        assert mission.rank_requirement == self.created_mission.rank_requirement
        assert mission.season_id == self.created_mission.season_id
        assert mission.category == self.created_mission.category

    async def test_get_mission_by_task_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_task(task_id=99999)

    async def test_get_mission_by_task_with_relations(self) -> None:
        inserted_task2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(
                title="Test Task 2",
                description="Test task 2 description",
            )
        )
        assert inserted_task2 is not None
        await self.storage.add_task_to_mission(
            mission_id=self.created_mission.id,
            task_id=inserted_task2.id,
        )

        mission = await self.storage.get_mission_by_task(task_id=self.created_task.id)

        assert len(mission.tasks) == 2
        assert mission.tasks[0].id == self.created_task.id
        assert mission.tasks[1].id == inserted_task2.id
