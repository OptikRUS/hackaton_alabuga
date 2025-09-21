import pytest

from src.core.ranks.exceptions import RankNotFoundError
from src.core.ranks.use_cases import GetRankDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetRankDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetRankDetailUseCase(storage=self.storage)

    async def test_get_rank_detail(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=1, name="Bronze", required_xp=100))

        rank = await self.use_case.execute(rank_id=1)

        assert rank == self.factory.rank(rank_id=1, name="Bronze", required_xp=100)

    async def test_get_rank_not_found(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.use_case.execute(rank_id=999)
