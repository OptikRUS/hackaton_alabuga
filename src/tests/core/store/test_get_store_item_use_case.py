import pytest

from src.core.store.exceptions import StoreItemNotFoundError
from src.core.store.use_cases import GetStoreItemUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetStoreItemUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetStoreItemUseCase(storage=self.storage)

    async def test_get_store_item_success(self) -> None:
        await self.storage.insert_store_item(
            self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=10,
            )
        )

        result = await self.use_case.execute(store_item_id=1)

        assert result == self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=10,
        )

    async def test_get_store_item_not_found_raises_error(self) -> None:
        with pytest.raises(StoreItemNotFoundError):
            await self.use_case.execute(store_item_id=999)
