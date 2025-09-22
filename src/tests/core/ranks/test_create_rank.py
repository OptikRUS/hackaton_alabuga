import pytest

from src.core.ranks.exceptions import RankNameAlreadyExistError
from src.core.ranks.use_cases import CreateRankUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateRankUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateRankUseCase(storage=self.storage)

    async def test_create_rank(self) -> None:
        rank = await self.use_case.execute(
            rank=self.factory.rank(rank_id=1, name="Bronze", required_xp=100)
        )

        assert rank == self.factory.rank(rank_id=1, name="Bronze", required_xp=100)

    async def test_create_rank_name_already_exist(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=0, name="Bronze", required_xp=100))

        with pytest.raises(RankNameAlreadyExistError):
            await self.use_case.execute(
                rank=self.factory.rank(rank_id=0, name="Bronze", required_xp=100)
            )
