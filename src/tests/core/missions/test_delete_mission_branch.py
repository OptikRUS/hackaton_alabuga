import pytest

from src.core.seasons.exceptions import SeasonNotFoundError
from src.core.seasons.use_cases import DeleteSeasonUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteSeasonUseCase(storage=self.storage)

    async def test_delete_season_success(self):
        await self.storage.insert_season(
            season=self.factory.season(season_id=1, name="Test Branch")
        )

        await self.use_case.execute(season_id=1)

        with pytest.raises(SeasonNotFoundError):
            await self.use_case.execute(season_id=1)

    async def test_delete_mission_branch_not_found(self):
        with pytest.raises(SeasonNotFoundError):
            await self.use_case.execute(season_id=999)
