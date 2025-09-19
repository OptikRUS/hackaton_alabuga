from httpx import codes

from src.tests.fixtures import APIFixture


class TestHealthAPI(APIFixture):
    def test_health(self) -> None:
        response = self.no_auth_api.get_health()

        assert response.is_success
        assert response.status_code == codes.OK
