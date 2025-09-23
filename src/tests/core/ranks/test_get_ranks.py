import pytest

from src.core.ranks.use_cases import GetRanksUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetRanksUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetRanksUseCase(storage=self.storage)

    async def test_get_ranks(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=1, name="Bronze", required_xp=100))
        await self.storage.insert_rank(self.factory.rank(rank_id=2, name="Silver", required_xp=200))

        ranks = await self.use_case.execute()

        assert len(ranks.values) == 2
        assert ranks.values[0] == self.factory.rank(rank_id=1, name="Bronze", required_xp=100)
        assert ranks.values[1] == self.factory.rank(rank_id=2, name="Silver", required_xp=200)
