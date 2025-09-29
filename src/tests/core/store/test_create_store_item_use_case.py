import pytest

from src.core.store.exceptions import StoreItemTitleAlreadyExistError
from src.core.store.use_cases import CreateStoreItemUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateStoreItemUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateStoreItemUseCase(storage=self.storage)

    async def test_create_store_item_success(self) -> None:
        result = await self.use_case.execute(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=10,
            )
        )

        assert result == self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=10,
        )

    async def test_create_store_item_with_existing_title_raises_error(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=10,
            )
        )

        with pytest.raises(StoreItemTitleAlreadyExistError):
            await self.use_case.execute(
                store_item=self.factory.store_item(
                    store_item_id=2,
                    title="Test Item",
                    price=200,
                    stock=5,
                )
            )

    async def test_create_store_item_with_different_titles_success(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="First Item",
                price=100,
                stock=10,
            )
        )

        result = await self.use_case.execute(
            store_item=self.factory.store_item(
                store_item_id=2,
                title="Different Item",
                price=200,
                stock=5,
            )
        )

        assert result == self.factory.store_item(
            store_item_id=2,
            title="Different Item",
            price=200,
            stock=5,
        )
