from dataclasses import dataclass

from httpx import Response
from starlette.testclient import TestClient


@dataclass
class APIHelper:
    client: TestClient

    def get_health(self) -> Response:
        return self.client.get("/health")

    def register_user(self, login: str, first_name: str, last_name: str, password: str) -> Response:
        return self.client.post(
            url="/users/register",
            json={
                "login": login,
                "firstName": first_name,
                "lastName": last_name,
                "password": password,
            },
        )

    def login_user(self, login: str, password: str) -> Response:
        return self.client.post(url="/users/login", json={"login": login, "password": password})

    def get_me(self) -> Response:
        return self.client.get("/users/me")

    def create_mission_branch(self, name: str) -> Response:
        return self.client.post(url="/missions/branches", json={"name": name})

    def list_mission_branches(self) -> Response:
        return self.client.get("/missions/branches")
