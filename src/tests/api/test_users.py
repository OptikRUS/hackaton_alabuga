import pytest
from httpx import codes

from src.core.exceptions import InvalidJWTTokenError
from src.core.users.enums import UserRoleEnum
from src.core.users.exceptions import (
    UserAlreadyExistError,
    UserIncorrectCredentialsError,
    UserNotFoundError,
)
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestUsersAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateUserUseCase)

    def test_user_registration(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.register_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CREATED

    def test_user_registration_already_exist(self) -> None:
        self.use_case.execute.side_effect = UserAlreadyExistError

        response = self.api.register_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": UserAlreadyExistError.detail}


class TestUserLoginAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(LoginUserUseCase)

    def test_user_login(self) -> None:
        self.use_case.execute.return_value = "token"

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.OK
        assert response.json() == {"token": "token"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_incorrect_credentials(self) -> None:
        self.use_case.execute.side_effect = UserIncorrectCredentialsError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.UNAUTHORIZED
        assert response.json() == {"detail": UserIncorrectCredentialsError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_invalid_jwt(self) -> None:
        self.use_case.execute.side_effect = InvalidJWTTokenError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.UNAUTHORIZED
        assert response.json() == {"detail": InvalidJWTTokenError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")


class TestGetMeAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetUserUseCase)

    async def test_get_me_no_auth(self) -> None:
        response = self.no_auth_api.get_me()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
            role=UserRoleEnum.CANDIDATE,
            exp=100,
            mana=150,
            rank_id=0,
        )

        response = self.api.get_me()

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "TEST",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
            "rankId": 0,
            "exp": 100,
            "mana": 150,
        }

    def test_get_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.api.get_me()

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
