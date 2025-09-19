import pytest

from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import GetUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetUserUseCase(storage=self.storage)

    async def test_get_user(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user = await self.use_case.execute(login="TEST")
        assert user == self.factory.user(
            login="TEST",
            password="TEST",
            first_name="TEST",
            last_name="TEST",
        )

    async def test_get_user_not_found(self) -> None:
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute(login="TEST")
