import pytest

from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionBranchStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_branch(branch=self.factory.mission_branch(name="TEST"))
        inserted_branch = await self.storage_helper.get_branch_by_name(name="TEST")
        assert inserted_branch is not None
        self.created_branch = inserted_branch.to_schema()

    async def test_update_mission_branch_success(self) -> None:
        updated_branch = self.factory.mission_branch(
            branch_id=self.created_branch.id,
            name="Updated Branch",
        )

        await self.storage.update_mission_branch(updated_branch)

        branch = await self.storage_helper.get_branch_by_name(name=updated_branch.name)

        assert branch is not None
        assert branch.id == self.created_branch.id
        assert branch.name == "Updated Branch"

    async def test_update_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.update_mission_branch(
                self.factory.mission_branch(branch_id=999, name="Non-existent Branch")
            )

    async def test_update_mission_branch_name_conflict(self) -> None:
        await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(branch_id=0, name="TEST2")
        )

        with pytest.raises(MissionBranchNameAlreadyExistError):
            await self.storage.update_mission_branch(
                self.factory.mission_branch(branch_id=self.created_branch.id, name="TEST2")
            )

    async def test_delete_mission_branch_success(self) -> None:
        await self.storage.delete_mission_branch(branch_id=self.created_branch.id)

        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.get_mission_branch_by_id(branch_id=self.created_branch.id)

    async def test_delete_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.storage.delete_mission_branch(branch_id=999)
