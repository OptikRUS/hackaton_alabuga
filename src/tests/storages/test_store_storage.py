import pytest

from src.core.store.exceptions import StoreItemNotFoundError, StoreItemTitleAlreadyExistError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestStoreStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def test_insert_store_item(self) -> None:
        store_item = self.factory.store_item(
            title="TEST_ITEM",
            price=100,
            stock=5,
        )

        await self.storage.insert_store_item(store_item=store_item)

        result = await self.storage_helper.get_store_item_by_title(title="TEST_ITEM")
        assert result is not None
        assert result.title == "TEST_ITEM"
        assert result.price == 100
        assert result.stock == 5

    async def test_insert_store_item_duplicate_title(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                title="TEST_ITEM",
                price=100,
                stock=5,
            )
        )

        with pytest.raises(StoreItemTitleAlreadyExistError):
            await self.storage.insert_store_item(
                store_item=self.factory.store_item(
                    title="TEST_ITEM",
                    price=200,
                    stock=10,
                )
            )

    async def test_get_store_item_by_id(self) -> None:
        inserted_item = await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="TEST_ITEM",
                price=100,
                stock=5,
            )
        )
        assert inserted_item is not None

        store_item = await self.storage.get_store_item_by_id(store_item_id=inserted_item.id)

        assert store_item.title == "TEST_ITEM"
        assert store_item.price == 100
        assert store_item.stock == 5

    async def test_get_store_item_by_id_not_found(self) -> None:
        with pytest.raises(StoreItemNotFoundError):
            await self.storage.get_store_item_by_id(store_item_id=999)

    async def test_get_store_item_by_title(self) -> None:
        await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="TEST_ITEM",
                price=100,
                stock=5,
            )
        )

        store_item = await self.storage.get_store_item_by_title(title="TEST_ITEM")

        assert store_item.title == "TEST_ITEM"
        assert store_item.price == 100
        assert store_item.stock == 5

    async def test_get_store_item_by_title_not_found(self) -> None:
        with pytest.raises(StoreItemNotFoundError):
            await self.storage.get_store_item_by_title(title="NON_EXISTENT")

    async def test_list_store_items(self) -> None:
        await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="ITEM_1",
                price=100,
                stock=5,
            )
        )
        await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="ITEM_2",
                price=200,
                stock=10,
            )
        )

        store_items = await self.storage.list_store_items()

        assert len(store_items.values) >= 2
        # TODO: нужно сравнить по индексу каждый типа store_items.values[0] и store_items.values[1]
        titles = [item.title for item in store_items.values]
        assert "ITEM_1" in titles
        assert "ITEM_2" in titles

    async def test_list_store_items_empty(self) -> None:
        store_items = await self.storage.list_store_items()
        assert len(store_items.values) == 0

    async def test_update_store_item(self) -> None:
        inserted_item = await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="TEST_ITEM",
                price=100,
                stock=5,
            )
        )
        assert inserted_item is not None

        updated_item = self.factory.store_item(
            store_item_id=inserted_item.id,
            title="UPDATED_ITEM",
            price=200,
            stock=10,
        )

        await self.storage.update_store_item(store_item=updated_item)

        result = await self.storage.get_store_item_by_id(store_item_id=inserted_item.id)
        assert result.title == "UPDATED_ITEM"
        assert result.price == 200
        assert result.stock == 10

    async def test_update_store_item_not_found(self) -> None:
        non_existent_item = self.factory.store_item(
            store_item_id=999,
            title="NON_EXISTENT",
            price=100,
            stock=5,
        )

        with pytest.raises(StoreItemNotFoundError):
            await self.storage.update_store_item(store_item=non_existent_item)

    async def test_update_store_item_duplicate_title(self) -> None:
        await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="ITEM_1",
                price=100,
                stock=5,
            )
        )
        inserted_item = await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="ITEM_2",
                price=200,
                stock=10,
            )
        )
        assert inserted_item is not None

        with pytest.raises(StoreItemTitleAlreadyExistError):
            await self.storage.update_store_item(
                store_item=self.factory.store_item(
                    store_item_id=inserted_item.id,
                    title="ITEM_1",
                    price=300,
                    stock=15,
                )
            )

    async def test_delete_store_item(self) -> None:
        inserted_item = await self.storage_helper.insert_store_item(
            store_item=self.factory.store_item(
                title="TEST_ITEM",
                price=100,
                stock=5,
            )
        )
        assert inserted_item is not None

        await self.storage.delete_store_item(store_item_id=inserted_item.id)

        result = await self.storage_helper.get_store_item_by_id(store_item_id=inserted_item.id)
        assert result is None

    async def test_delete_store_item_not_found(self) -> None:
        with pytest.raises(StoreItemNotFoundError):
            await self.storage.delete_store_item(store_item_id=999)
