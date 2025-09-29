from dataclasses import dataclass

from src.core.storages import StoreStorage
from src.core.store.exceptions import StoreItemNotFoundError, StoreItemTitleAlreadyExistError
from src.core.store.schemas import StoreItem, StoreItems
from src.core.use_case import UseCase


@dataclass
class CreateStoreItemUseCase(UseCase):
    storage: StoreStorage

    async def execute(self, store_item: StoreItem) -> StoreItem:
        try:
            await self.storage.get_store_item_by_title(title=store_item.title)
            raise StoreItemTitleAlreadyExistError
        except StoreItemNotFoundError:
            await self.storage.insert_store_item(store_item=store_item)
            return await self.storage.get_store_item_by_title(title=store_item.title)


@dataclass
class GetStoreItemsUseCase(UseCase):
    storage: StoreStorage

    async def execute(self) -> StoreItems:
        return await self.storage.list_store_items()


@dataclass
class GetStoreItemUseCase(UseCase):
    storage: StoreStorage

    async def execute(self, store_item_id: int) -> StoreItem:
        return await self.storage.get_store_item_by_id(store_item_id=store_item_id)


@dataclass
class UpdateStoreItemUseCase(UseCase):
    storage: StoreStorage

    async def execute(self, store_item: StoreItem) -> StoreItem:
        await self.storage.get_store_item_by_id(store_item_id=store_item.id)
        await self.storage.update_store_item(store_item=store_item)
        return await self.storage.get_store_item_by_id(store_item_id=store_item.id)


@dataclass
class DeleteStoreItemUseCase(UseCase):
    storage: StoreStorage

    async def execute(self, store_item_id: int) -> None:
        await self.storage.get_store_item_by_id(store_item_id=store_item_id)
        await self.storage.delete_store_item(store_item_id=store_item_id)
