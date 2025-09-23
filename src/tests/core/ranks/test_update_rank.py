import pytest

from src.core.ranks.exceptions import RankNameAlreadyExistError, RankNotFoundError
from src.core.ranks.use_cases import UpdateRankUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateRankUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateRankUseCase(storage=self.storage)

    async def test_update_rank(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=1, name="Bronze", required_xp=100))

        updated = await self.use_case.execute(
            rank=self.factory.rank(rank_id=1, name="Bronze+", required_xp=150)
        )

        assert updated == self.factory.rank(rank_id=1, name="Bronze+", required_xp=150)

    async def test_update_rank_name_already_exists(self) -> None:
        await self.storage.insert_rank(self.factory.rank(rank_id=1, name="Bronze", required_xp=100))
        await self.storage.insert_rank(self.factory.rank(rank_id=2, name="Silver", required_xp=200))

        with pytest.raises(RankNameAlreadyExistError):
            await self.use_case.execute(
                rank=self.factory.rank(rank_id=2, name="Bronze", required_xp=200)
            )

    async def test_update_rank_not_found(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.use_case.execute(
                rank=self.factory.rank(rank_id=999, name="X", required_xp=1)
            )
