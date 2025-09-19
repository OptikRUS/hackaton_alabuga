import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionAlreadyExistError, MissionNotFoundError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def _create_test_branch(self) -> int:
        await self.storage_helper.insert_branch(
            branch=(self.factory.mission_branch(branch_id=0, name="TEST_BRANCH"))
        )

        stored_branch = await self.storage_helper.get_branch_by_name(name="TEST_BRANCH")

        assert stored_branch is not None
        return stored_branch.id

    async def test_get_mission_by_id(self) -> None:
        branch_id = await self._create_test_branch()

        inserted_mission = await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=0,
                    title="TEST_MISSION",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=branch_id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )
        assert inserted_mission is not None

        result = await self.storage.get_mission_by_id(mission_id=inserted_mission.id)

        assert result is not None
        assert result.title == "TEST_MISSION"
        assert result.description == "Test description"
        assert result.reward_xp == 100
        assert result.reward_mana == 50
        assert result.rank_requirement == 1
        assert result.branch_id == branch_id
        assert result.category == MissionCategoryEnum.QUEST

    async def test_get_mission_by_id_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_id(mission_id=999)

    async def test_get_mission_by_title(self) -> None:
        branch_id = await self._create_test_branch()

        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=branch_id,
            category=MissionCategoryEnum.QUEST,
        )
        await self.storage_helper.insert_mission(mission=mission)

        result = await self.storage.get_mission_by_title(title="TEST_MISSION")

        assert result is not None
        assert result.title == "TEST_MISSION"
        assert result.description == "Test description"
        assert result.reward_xp == 100
        assert result.reward_mana == 50
        assert result.rank_requirement == 1
        assert result.branch_id == branch_id
        assert result.category == MissionCategoryEnum.QUEST

    async def test_get_mission_by_title_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_title(title="NON_EXISTENT")

    async def test_insert_mission(self) -> None:
        branch_id = await self._create_test_branch()

        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=branch_id,
            category=MissionCategoryEnum.QUEST,
        )

        await self.storage.insert_mission(mission=mission)

        result = await self.storage_helper.get_mission_by_title(title="TEST_MISSION")
        assert result is not None
        assert result.title == "TEST_MISSION"
        assert result.description == "Test description"
        assert result.reward_xp == 100
        assert result.reward_mana == 50
        assert result.rank_requirement == 1
        assert result.branch_id == branch_id
        assert result.category == MissionCategoryEnum.QUEST

    async def test_insert_mission_already_exist(self) -> None:
        branch_id = await self._create_test_branch()

        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=branch_id,
            category=MissionCategoryEnum.QUEST,
        )
        await self.storage_helper.insert_mission(mission=mission)

        with pytest.raises(MissionAlreadyExistError):
            await self.storage.insert_mission(mission=mission)

    async def test_list_missions(self) -> None:
        branch_id = await self._create_test_branch()

        mission1 = self.factory.mission(
            mission_id=0,
            title="MISSION_1",
            description="Description 1",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=branch_id,
            category=MissionCategoryEnum.QUEST,
        )
        mission2 = self.factory.mission(
            mission_id=0,
            title="MISSION_2",
            description="Description 2",
            reward_xp=200,
            reward_mana=100,
            rank_requirement=2,
            branch_id=branch_id,
            category=MissionCategoryEnum.LECTURE,
        )

        await self.storage_helper.insert_mission(mission=mission1)
        await self.storage_helper.insert_mission(mission=mission2)

        missions = await self.storage.list_missions()

        assert len(missions.values) == 2
        missions.values[0].title = "MISSION_1"
        missions.values[0].description = "Description 1"
        missions.values[0].reward_xp = 100
        missions.values[0].reward_mana = 50
        missions.values[0].rank_requirement = 1
        missions.values[0].branch_id = branch_id
        missions.values[0].category = MissionCategoryEnum.QUEST
        missions.values[1].title = "MISSION_2"
        missions.values[1].description = "Description 2"
        missions.values[1].reward_xp = 200
        missions.values[1].reward_mana = 100
        missions.values[1].rank_requirement = 2
        missions.values[1].branch_id = branch_id
        missions.values[1].category = MissionCategoryEnum.LECTURE

    async def test_list_empty_missions(self) -> None:
        result = await self.storage.list_missions()

        assert len(result.values) == 0

    async def test_update_mission(self) -> None:
        branch_id = await self._create_test_branch()

        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=0,
                    title="ORIGINAL_MISSION",
                    description="Original description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=branch_id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        stored_mission = await self.storage_helper.get_mission_by_title(title="ORIGINAL_MISSION")
        assert stored_mission is not None

        updated_mission = self.factory.mission(
            mission_id=stored_mission.id,
            title="UPDATED_MISSION",
            description="Updated description",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=branch_id,
            category=MissionCategoryEnum.LECTURE,
        )

        await self.storage.update_mission(mission=updated_mission)

        result = await self.storage_helper.get_mission_by_id(mission_id=stored_mission.id)
        assert result is not None
        assert result.title == "UPDATED_MISSION"
        assert result.description == "Updated description"
        assert result.reward_xp == 150
        assert result.reward_mana == 75
        assert result.rank_requirement == 2
        assert result.branch_id == branch_id
        assert result.category == MissionCategoryEnum.LECTURE

    async def test_delete_mission(self) -> None:
        branch_id = await self._create_test_branch()

        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=branch_id,
            category=MissionCategoryEnum.LECTURE,
        )
        await self.storage_helper.insert_mission(mission=mission)
        stored_mission = await self.storage_helper.get_mission_by_title(title="TEST_MISSION")
        assert stored_mission is not None

        await self.storage.delete_mission(mission_id=stored_mission.id)

        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_id(mission_id=stored_mission.id)

    async def test_delete_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.delete_mission(mission_id=999)
