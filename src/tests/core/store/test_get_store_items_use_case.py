import pytest

from src.core.store.use_cases import GetStoreItemsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetStoreItemsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetStoreItemsUseCase(storage=self.storage)

    async def test_get_store_items_empty_list(self) -> None:
        result = await self.use_case.execute()

        assert result == self.factory.store_items(values=[])

    async def test_get_store_items_with_items(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Item 1",
                price=100,
                stock=10,
            )
        )
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=2,
                title="Item 2",
                price=200,
                stock=5,
            )
        )

        result = await self.use_case.execute()

        assert result == self.factory.store_items(
            values=[
                self.factory.store_item(
                    store_item_id=1,
                    title="Item 1",
                    price=100,
                    stock=10,
                ),
                self.factory.store_item(
                    store_item_id=2,
                    title="Item 2",
                    price=200,
                    stock=5,
                ),
            ]
        )
