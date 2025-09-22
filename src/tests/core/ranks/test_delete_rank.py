import pytest

from src.core.ranks.exceptions import RankNotFoundError
from src.core.ranks.use_cases import DeleteRankUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteRankUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteRankUseCase(storage=self.storage)

    async def test_delete_rank(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=1, name="Bronze", required_xp=100))

        await self.use_case.execute(rank_id=1)

        with pytest.raises(RankNotFoundError):
            await self.storage.get_rank_by_id(rank_id=1)

    async def test_delete_rank_not_found(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.use_case.execute(rank_id=999)
