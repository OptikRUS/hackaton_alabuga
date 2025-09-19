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

    def get_mission_branches(self) -> Response:
        return self.client.get("/missions/branches")

    def update_mission_branch(self, branch_id: int, name: str) -> Response:
        return self.client.put(url=f"/missions/branches/{branch_id}", json={"name": name})

    def delete_mission_branch(self, branch_id: int) -> Response:
        return self.client.delete(f"/missions/branches/{branch_id}")

    def create_mission(
        self,
        title: str,
        description: str,
        reward_xp: int,
        reward_mana: int,
        rank_requirement: int,
        branch_id: int,
        category: str,
    ) -> Response:
        return self.client.post(
            url="/missions",
            json={
                "title": title,
                "description": description,
                "rewardXp": reward_xp,
                "rewardMana": reward_mana,
                "rankRequirement": rank_requirement,
                "branchId": branch_id,
                "category": category,
            },
        )

    def get_missions(self) -> Response:
        return self.client.get("/missions")

    def get_mission(self, mission_id: int) -> Response:
        return self.client.get(f"/missions/{mission_id}")

    def update_mission(
        self,
        mission_id: int,
        title: str,
        description: str,
        reward_xp: int,
        reward_mana: int,
        rank_requirement: int,
        branch_id: int,
        category: str,
    ) -> Response:
        return self.client.put(
            url=f"/missions/{mission_id}",
            json={
                "title": title,
                "description": description,
                "rewardXp": reward_xp,
                "rewardMana": reward_mana,
                "rankRequirement": rank_requirement,
                "branchId": branch_id,
                "category": category,
            },
        )

    def delete_mission(self, mission_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}")

    def create_task(self, title: str, description: str) -> Response:
        return self.client.post(
            url="/tasks",
            json={
                "title": title,
                "description": description,
            },
        )

    def get_tasks(self) -> Response:
        return self.client.get("/tasks")

    def get_task(self, task_id: int) -> Response:
        return self.client.get(f"/tasks/{task_id}")

    def update_task(self, task_id: int, title: str, description: str) -> Response:
        return self.client.put(
            url=f"/tasks/{task_id}",
            json={
                "title": title,
                "description": description,
            },
        )

    def delete_task(self, task_id: int) -> Response:
        return self.client.delete(f"/tasks/{task_id}")

    def add_task_to_mission(self, mission_id: int, task_id: int) -> Response:
        return self.client.post(f"/missions/{mission_id}/tasks/{task_id}")

    def remove_task_from_mission(self, mission_id: int, task_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}/tasks/{task_id}")
