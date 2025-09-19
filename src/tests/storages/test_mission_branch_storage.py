import pytest

from src.core.missions.exceptions import (
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionBranchStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def _create_test_branch(self, name: str = "TEST_BRANCH") -> int:
        await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(branch_id=0, name=name)
        )

        stored_branch = await self.storage_helper.get_branch_by_name(name=name)
        assert stored_branch is not None
        return stored_branch.id

    async def test_update_mission_branch_success(self) -> None:
        branch_id = await self._create_test_branch("Original Branch")
        updated_branch = self.factory.mission_branch(branch_id=branch_id, name="Updated Branch")

        await self.storage.update_mission_branch(updated_branch)

        branch = await self.storage_helper.get_branch_by_name(name=updated_branch.name)

        assert branch is not None
        assert branch.name == "Updated Branch"

    async def test_update_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.update_mission_branch(
                self.factory.mission_branch(branch_id=999, name="Non-existent Branch")
            )

    async def test_update_mission_branch_name_conflict(self) -> None:
        branch_id1 = await self._create_test_branch(name="TEST1")
        await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(branch_id=0, name="TEST2")
        )

        with pytest.raises(MissionBranchAlreadyExistError):
            await self.storage.update_mission_branch(
                self.factory.mission_branch(branch_id=branch_id1, name="TEST2")
            )

    async def test_delete_mission_branch_success(self) -> None:
        branch_id = await self._create_test_branch("Test Branch")

        await self.storage.delete_mission_branch(branch_id=branch_id)

        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.get_mission_branch_by_id(branch_id=branch_id)

    async def test_delete_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.delete_mission_branch(branch_id=999)
