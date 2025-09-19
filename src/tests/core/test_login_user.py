import pytest

from src.core.users.exceptions import UserIncorrectCredentialsError, UserNotFoundError
from src.core.users.use_cases import LoginUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock
from src.tests.mocks.user_password import UserPasswordServiceMock


class TestLoginUserUseCaseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.password_service = UserPasswordServiceMock()
        self.use_case = LoginUserUseCase(
            storage=self.storage,
            password_service=self.password_service,
        )

    async def test_login_user(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        token = await self.use_case.execute(login="TEST", password="TEST")

        assert token == "{'login': 'TEST'}"  # noqa: S105

    async def test_login_user_not_found(self) -> None:
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute(login="TEST", password="TEST")

    async def test_login_user_incorrect_password(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )
        self.storage.user_table["TEST"] = self.factory.user(
            login="TEST",
            password="WRONG",
            first_name="TEST",
            last_name="TEST",
        )

        with pytest.raises(UserIncorrectCredentialsError):
            await self.use_case.execute(login="TEST", password="TEST")
