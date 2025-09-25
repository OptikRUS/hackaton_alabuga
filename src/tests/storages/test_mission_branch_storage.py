import pytest

from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionBranchStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_season(season=self.factory.season(name="TEST"))
        inserted_branch = await self.storage_helper.get_branch_by_name(name="TEST")
        assert inserted_branch is not None
        self.created_branch = inserted_branch.to_schema()

    async def test_update_mission_branch_success(self) -> None:
        updated_branch = self.factory.season(
            season_id=self.created_branch.id,
            name="Updated Branch",
        )

        await self.storage.update_season(updated_branch)

        branch = await self.storage_helper.get_branch_by_name(name=updated_branch.name)

        assert branch is not None
        assert branch.id == self.created_branch.id
        assert branch.name == "Updated Branch"

    async def test_update_mission_branch_not_found(self) -> None:
        with pytest.raises(SeasonNotFoundError):
            await self.storage.update_season(
                self.factory.season(season_id=999, name="Non-existent Branch")
            )

    async def test_update_mission_branch_name_conflict(self) -> None:
        await self.storage_helper.insert_season(
            season=self.factory.season(season_id=0, name="TEST2")
        )

        with pytest.raises(SeasonNameAlreadyExistError):
            await self.storage.update_season(
                self.factory.season(season_id=self.created_branch.id, name="TEST2")
            )

    async def test_delete_mission_branch_success(self) -> None:
        await self.storage.delete_season(season_id=self.created_branch.id)

        with pytest.raises(SeasonNotFoundError):
            await self.storage.get_season_by_id(season_id=self.created_branch.id)

    async def test_delete_mission_branch_not_found(self) -> None:
        with pytest.raises(SeasonNotFoundError):
            await self.storage.delete_season(season_id=999)
