import pytest

from src.core.missions.exceptions import MissionBranchAlreadyExistError
from src.core.missions.schemas import MissionBranch
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionBranchStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def test_insert_branch(self) -> None:
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(
                name="TEST",
            )
        )

        exp_branch = await self.storage_helper.get_branch_by_name(name="TEST")

        assert exp_branch is not None
        assert exp_branch.name == "TEST"

    async def test_insert_branch_duplicate(self) -> None:
        await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(branch_id=0, name="TEST")
        )
        with pytest.raises(MissionBranchAlreadyExistError):
            await self.storage.insert_mission_branch(MissionBranch(id=0, name="TEST"))

    async def test_list_branches(self) -> None:
        await self.storage.insert_mission_branch(MissionBranch(id=0, name="TEST1"))
        await self.storage.insert_mission_branch(MissionBranch(id=0, name="TEST2"))

        mission_branches = await self.storage.list_mission_branches()

        assert mission_branches.values[0].name == "TEST1"
        assert mission_branches.values[1].name == "TEST2"
