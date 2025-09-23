import pytest

from src.core.users.exceptions import UserAlreadyExistError
from src.core.users.use_cases import CreateUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock
from src.tests.mocks.user_password import UserPasswordServiceMock


class TestCreateUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.password_service = UserPasswordServiceMock()
        self.use_case = CreateUserUseCase(
            storage=self.storage,
            password_service=self.password_service,
        )

    async def test_create_user(self) -> None:
        await self.use_case.execute(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

    async def test_create_user_already_exists(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        with pytest.raises(UserAlreadyExistError):
            await self.use_case.execute(
                user=self.factory.user(
                    login="TEST",
                    password="TEST",
                    first_name="TEST",
                    last_name="TEST",
                )
            )
