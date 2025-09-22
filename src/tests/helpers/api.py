from dataclasses import dataclass
from io import BytesIO

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
            json={"title": title, "description": description},
        )

    def get_tasks(self) -> Response:
        return self.client.get("/tasks")

    def get_task(self, task_id: int) -> Response:
        return self.client.get(f"/tasks/{task_id}")

    def update_task(self, task_id: int, title: str, description: str) -> Response:
        return self.client.put(
            url=f"/tasks/{task_id}",
            json={"title": title, "description": description},
        )

    def delete_task(self, task_id: int) -> Response:
        return self.client.delete(f"/tasks/{task_id}")

    def add_task_to_mission(self, mission_id: int, task_id: int) -> Response:
        return self.client.post(f"/missions/{mission_id}/tasks/{task_id}")

    def remove_task_from_mission(self, mission_id: int, task_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}/tasks/{task_id}")

    def create_artifact(
        self,
        title: str,
        description: str,
        rarity: str,
        image_url: str,
    ) -> Response:
        return self.client.post(
            url="/artifacts",
            json={
                "title": title,
                "description": description,
                "rarity": rarity,
                "image_url": image_url,
            },
        )

    def get_artifacts(self) -> Response:
        return self.client.get("/artifacts")

    def get_artifact(self, artifact_id: int) -> Response:
        return self.client.get(f"/artifacts/{artifact_id}")

    def update_artifact(
        self,
        artifact_id: int,
        title: str,
        description: str,
        rarity: str,
        image_url: str,
    ) -> Response:
        return self.client.put(
            url=f"/artifacts/{artifact_id}",
            json={
                "title": title,
                "description": description,
                "rarity": rarity,
                "image_url": image_url,
            },
        )

    def delete_artifact(self, artifact_id: int) -> Response:
        return self.client.delete(f"/artifacts/{artifact_id}")

    def add_artifact_to_mission(self, mission_id: int, artifact_id: int) -> Response:
        return self.client.post(f"/missions/{mission_id}/artifacts/{artifact_id}")

    def remove_artifact_from_mission(self, mission_id: int, artifact_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}/artifacts/{artifact_id}")

    def add_artifact_to_user(self, user_login: str, artifact_id: int) -> Response:
        return self.client.post(f"/users/{user_login}/artifacts/{artifact_id}")

    def remove_artifact_from_user(self, user_login: str, artifact_id: int) -> Response:
        return self.client.delete(f"/users/{user_login}/artifacts/{artifact_id}")

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str = "text/plain",
    ) -> Response:
        return self.client.post(
            url="/media",
            files={"file": (filename, BytesIO(file_content), content_type)},
        )

    def download_file(self, key: str) -> Response:
        return self.client.get(f"/media/{key}")

    # Skills endpoints
    def create_skill(self, name: str, max_level: int) -> Response:
        return self.client.post(
            url="/skills",
            json={"name": name, "max_level": max_level},
        )

    def get_skills(self) -> Response:
        return self.client.get("/skills")

    def get_skill(self, skill_id: int) -> Response:
        return self.client.get(f"/skills/{skill_id}")

    def update_skill(self, skill_id: int, name: str, max_level: int) -> Response:
        return self.client.put(
            url=f"/skills/{skill_id}",
            json={"name": name, "max_level": max_level},
        )

    def delete_skill(self, skill_id: int) -> Response:
        return self.client.delete(f"/skills/{skill_id}")

    # Competitions endpoints
    def create_competition(self, name: str, max_level: int) -> Response:
        return self.client.post(
            url="/competitions",
            json={"name": name, "max_level": max_level},
        )

    def get_competitions(self) -> Response:
        return self.client.get("/competitions")

    def get_competition(self, competition_id: int) -> Response:
        return self.client.get(f"/competitions/{competition_id}")

    def update_competition(self, competition_id: int, name: str, max_level: int) -> Response:
        return self.client.put(
            url=f"/competitions/{competition_id}",
            json={"name": name, "max_level": max_level},
        )

    def delete_competition(self, competition_id: int) -> Response:
        return self.client.delete(f"/competitions/{competition_id}")

    def add_skill_to_competition(self, competition_id: int, skill_id: int) -> Response:
        return self.client.post(f"/competitions/{competition_id}/skills/{skill_id}")

    def remove_skill_from_competition(self, competition_id: int, skill_id: int) -> Response:
        return self.client.delete(f"/competitions/{competition_id}/skills/{skill_id}")
