import pytest

from src.core.store.exceptions import (
    InsufficientManaError,
    StoreItemInsufficientStockError,
    StoreItemNotFoundError,
)
from src.core.store.use_cases import PurchaseStoreItemUseCase
from src.core.users.exceptions import UserNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestPurchaseStoreItemUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = PurchaseStoreItemUseCase(
            store_storage=self.storage,
            user_storage=self.storage,
        )

    async def test_purchase_store_item_success(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=5,
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=200,
            )
        )
        result = await self.use_case.execute(
            purchase=self.factory.store_purchase(
                user_login="test_user",
                store_item_id=1,
            )
        )

        assert result == self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=4,  # Уменьшилось на 1
        )
        updated_user = await self.storage.get_candidate_by_login(login="test_user")
        assert updated_user.mana == 100  # 200 - 100

    async def test_purchase_store_item_insufficient_stock_raises_error(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=0,
            )
        )

        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=200,
            )
        )

        with pytest.raises(StoreItemInsufficientStockError):
            await self.use_case.execute(
                purchase=self.factory.store_purchase(
                    user_login="test_user",
                    store_item_id=1,
                )
            )

    async def test_purchase_store_item_insufficient_mana_raises_error(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=200,
                stock=5,
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=100,  # Недостаточно маны
            )
        )
        with pytest.raises(InsufficientManaError):
            await self.use_case.execute(
                purchase=self.factory.store_purchase(
                    user_login="test_user",
                    store_item_id=1,
                )
            )

    async def test_purchase_store_item_not_found_raises_error(self) -> None:
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=200,
            )
        )
        with pytest.raises(StoreItemNotFoundError):
            await self.use_case.execute(
                purchase=self.factory.store_purchase(
                    user_login="test_user",
                    store_item_id=999,
                )
            )

    async def test_purchase_store_item_user_not_found_raises_error(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=5,
            )
        )
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute(
                purchase=self.factory.store_purchase(
                    user_login="nonexistent_user",
                    store_item_id=1,
                )
            )

    async def test_purchase_store_item_exact_mana_success(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=100,
                stock=5,
            )
        )

        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=100,  # Точно столько, сколько нужно
            )
        )
        result = await self.use_case.execute(
            purchase=self.factory.store_purchase(
                user_login="test_user",
                store_item_id=1,
            )
        )

        assert result == self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=4,
        )
        updated_user = await self.storage.get_candidate_by_login(login="test_user")
        assert updated_user.mana == 0

    async def test_purchase_store_item_multiple_purchases(self) -> None:
        await self.storage.insert_store_item(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Test Item",
                price=50,
                stock=3,
            )
        )
        await self.storage.insert_user(
            user=self.factory.candidate(
                login="test_user",
                password="password",
                mana=200,
            )
        )

        result1 = await self.use_case.execute(
            purchase=self.factory.store_purchase(
                user_login="test_user",
                store_item_id=1,
            )
        )

        assert result1.stock == 2
        user_after_first = await self.storage.get_candidate_by_login(login="test_user")
        assert user_after_first.mana == 150

        result2 = await self.use_case.execute(
            purchase=self.factory.store_purchase(
                user_login="test_user",
                store_item_id=1,
            )
        )

        assert result2.stock == 1
        user_after_second = await self.storage.get_candidate_by_login(login="test_user")
        assert user_after_second.mana == 100

        result3 = await self.use_case.execute(
            purchase=self.factory.store_purchase(
                user_login="test_user",
                store_item_id=1,
            )
        )

        assert result3.stock == 0
        user_after_third = await self.storage.get_candidate_by_login(login="test_user")
        assert user_after_third.mana == 50

        with pytest.raises(StoreItemInsufficientStockError):
            await self.use_case.execute(
                purchase=self.factory.store_purchase(
                    user_login="test_user",
                    store_item_id=1,
                )
            )
