import pytest
from httpx import codes

from src.core.artifacts.exceptions import ArtifactNotFoundError
from src.core.artifacts.use_cases import (
    AddArtifactToUserUseCase,
    RemoveArtifactFromUserUseCase,
)
from src.core.exceptions import InvalidJWTTokenError, PermissionDeniedError
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

    def test_hr_registration(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.register_hr_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.hr_user(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_candidate_registration(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.register_candidate_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.candidate(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_hr_registration_already_exists(self) -> None:
        self.use_case.execute.side_effect = UserAlreadyExistError

        response = self.api.register_hr_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": UserAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.hr_user(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_candidate_registration_already_exists(self) -> None:
        self.use_case.execute.side_effect = UserAlreadyExistError

        response = self.api.register_candidate_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": UserAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.candidate(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )


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

    def test_user_permission_denied_error(self) -> None:
        self.use_case.execute.side_effect = PermissionDeniedError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")


class TestGetMeAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetUserUseCase)

    async def test_get_me_no_auth(self) -> None:
        response = self.api.get_me()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.get_me()

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="hr_user")


class TestAddArtifactToUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddArtifactToUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_artifact_to_user(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="testuser",
            password="password",
            role=UserRoleEnum.CANDIDATE,
        )

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_add_artifact_to_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_add_artifact_to_user_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)


class TestRemoveArtifactFromUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveArtifactFromUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_artifact_from_user(
            user_login="testuser", artifact_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_remove_artifact_from_user(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="testuser",
            password="password",
            role=UserRoleEnum.CANDIDATE,
        )

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_remove_artifact_from_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_remove_artifact_from_user_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)
