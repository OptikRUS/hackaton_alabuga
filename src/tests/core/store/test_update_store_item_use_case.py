import pytest

from src.core.store.exceptions import StoreItemNotFoundError
from src.core.store.use_cases import UpdateStoreItemUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateStoreItemUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateStoreItemUseCase(storage=self.storage)

    async def test_update_store_item_success(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Original Item",
                price=100,
                stock=10,
            )
        )

        result = await self.use_case.execute(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Updated Item",
                price=200,
                stock=5,
            )
        )

        assert result == self.factory.store_item(
            store_item_id=1,
            title="Updated Item",
            price=200,
            stock=5,
        )

    async def test_update_store_item_not_found_raises_error(self) -> None:
        with pytest.raises(StoreItemNotFoundError):
            await self.use_case.execute(
                store_item=self.factory.store_item(
                    store_item_id=999,
                    title="Non-existent Item",
                    price=100,
                    stock=10,
                )
            )
