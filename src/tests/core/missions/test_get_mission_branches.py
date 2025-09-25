import pytest

from src.core.seasons.use_cases import GetSeasonsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionBranchesUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetSeasonsUseCase(storage=self.storage)

    async def test_get_mission_branches(self) -> None:
        await self.storage.insert_season(season=self.factory.season(season_id=1, name="TEST1"))
        await self.storage.insert_season(season=self.factory.season(season_id=2, name="TEST2"))

        branches = await self.use_case.execute()

        assert len(branches.values) == 2
        assert branches == self.factory.seasons(
            values=[
                self.factory.season(season_id=1, name="TEST1"),
                self.factory.season(season_id=2, name="TEST2"),
            ]
        )

    async def test_get_empty_mission_branches(self) -> None:
        result = await self.use_case.execute()

        assert len(result.values) == 0
