import pytest

from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.use_cases import UpdateSeasonUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateSeasonUseCase(storage=self.storage)

    async def test_update_season_success(self):
        await self.storage.insert_season(
            season=self.factory.season(
                season_id=1,
                name="Original Branch",
                start_date="2025-11-25T06:55:47Z",
                end_date="2025-11-25T06:55:47Z",
            ),
        )

        season = await self.use_case.execute(
            season=self.factory.season(season_id=1, name="Updated Branch")
        )

        assert season == self.factory.season(season_id=1, name="Updated Branch")

    async def test_update_season_not_found(self):
        with pytest.raises(SeasonNotFoundError):
            await self.use_case.execute(season=self.factory.season(season_id=1, name="TEST"))

    async def test_update_mission_branch_name_conflict(self):
        await self.storage.insert_season(season=self.factory.season(season_id=1, name="TEST1"))
        await self.storage.insert_season(season=self.factory.season(season_id=2, name="TEST2"))

        with pytest.raises(SeasonNameAlreadyExistError):
            await self.use_case.execute(season=self.factory.season(season_id=1, name="TEST2"))

    async def test_update_mission_branch_same_name(self):
        await self.storage.insert_season(
            season=self.factory.season(season_id=1, name="Test Branch")
        )

        season = await self.use_case.execute(
            season=self.factory.season(season_id=1, name="Test Branch")
        )

        assert season == self.factory.season(season_id=1, name="Test Branch")
