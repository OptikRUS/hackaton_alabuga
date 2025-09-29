import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.store.exceptions import StoreItemNotFoundError, StoreItemTitleAlreadyExistError
from src.core.store.use_cases import (
    CreateStoreItemUseCase,
    DeleteStoreItemUseCase,
    GetStoreItemsUseCase,
    GetStoreItemUseCase,
    UpdateStoreItemUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateStoreItemAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateStoreItemUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_store_item(title="Test Item", price=100, stock=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_store_item(title="Test Item", price=100, stock=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_store_item_success(self) -> None:
        self.use_case.execute.return_value = self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=10,
        )

        response = self.hr_api.create_store_item(title="Test Item", price=100, stock=10)

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "title": "Test Item",
            "price": 100,
            "stock": 10,
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            store_item=self.factory.store_item(
                store_item_id=0,
                title="Test Item",
                price=100,
                stock=10,
            )
        )

    def test_create_store_item_title_already_exists(self) -> None:
        self.use_case.execute.side_effect = StoreItemTitleAlreadyExistError

        response = self.hr_api.create_store_item(title="Test Item", price=100, stock=10)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": StoreItemTitleAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            store_item=self.factory.store_item(
                store_item_id=0,
                title="Test Item",
                price=100,
                stock=10,
            )
        )


class TestGetStoreItemsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetStoreItemsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_store_items()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_store_items_success(self) -> None:
        self.use_case.execute.return_value = self.factory.store_items([
            self.factory.store_item(
                store_item_id=1,
                title="Test Item 1",
                price=100,
                stock=10,
            ),
            self.factory.store_item(
                store_item_id=2,
                title="Test Item 2",
                price=200,
                stock=5,
            ),
        ])

        response = self.hr_api.get_store_items()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "title": "Test Item 1",
                    "price": 100,
                    "stock": 10,
                },
                {
                    "id": 2,
                    "title": "Test Item 2",
                    "price": 200,
                    "stock": 5,
                },
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_store_items_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.store_items([])

        response = self.candidate_api.get_store_items()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


class TestGetStoreItemAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetStoreItemUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_store_item(store_item_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_store_item_success(self) -> None:
        self.use_case.execute.return_value = self.factory.store_item(
            store_item_id=1,
            title="Test Item",
            price=100,
            stock=10,
        )

        response = self.hr_api.get_store_item(store_item_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Item",
            "price": 100,
            "stock": 10,
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(store_item_id=1)

    def test_get_store_item_not_found(self) -> None:
        self.use_case.execute.side_effect = StoreItemNotFoundError

        response = self.candidate_api.get_store_item(store_item_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": StoreItemNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(store_item_id=999)


class TestUpdateStoreItemAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateStoreItemUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_store_item(
            store_item_id=1,
            title="Updated Item",
            price=150,
            stock=20,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_store_item(
            store_item_id=1,
            title="Updated Item",
            price=150,
            stock=20,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_store_item_success(self) -> None:
        self.use_case.execute.return_value = self.factory.store_item(
            store_item_id=1,
            title="Updated Item",
            price=150,
            stock=20,
        )

        response = self.hr_api.update_store_item(
            store_item_id=1,
            title="Updated Item",
            price=150,
            stock=20,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Updated Item",
            "price": 150,
            "stock": 20,
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            store_item=self.factory.store_item(
                store_item_id=1,
                title="Updated Item",
                price=150,
                stock=20,
            )
        )

    def test_update_store_item_not_found(self) -> None:
        self.use_case.execute.side_effect = StoreItemNotFoundError

        response = self.hr_api.update_store_item(
            store_item_id=999, title="Updated Item", price=150, stock=20
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": StoreItemNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            store_item=self.factory.store_item(
                store_item_id=999,
                title="Updated Item",
                price=150,
                stock=20,
            )
        )


class TestDeleteStoreItemAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteStoreItemUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_store_item(store_item_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_store_item(store_item_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_store_item_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_store_item(store_item_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(store_item_id=1)

    def test_delete_store_item_not_found(self) -> None:
        self.use_case.execute.side_effect = StoreItemNotFoundError

        response = self.hr_api.delete_store_item(store_item_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": StoreItemNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(store_item_id=999)
