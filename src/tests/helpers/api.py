from dataclasses import dataclass
from io import BytesIO

from httpx import Response
from starlette.testclient import TestClient

from src.core.artifacts.enums import ArtifactRarityEnum


@dataclass
class APIHelper:
    client: TestClient

    def get_health(self) -> Response:
        return self.client.get("/health")

    def register_hr_user(
        self, login: str, first_name: str, last_name: str, password: str
    ) -> Response:
        return self.client.post(
            url="/users/register",
            json={
                "login": login,
                "firstName": first_name,
                "lastName": last_name,
                "password": password,
            },
        )

    def register_candidate_user(
        self, login: str, first_name: str, last_name: str, password: str
    ) -> Response:
        return self.client.post(
            url="/mobile/users/register",
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

    def create_season(self, name: str, start_date: str, end_date: str) -> Response:
        return self.client.post(
            url="/seasons",
            json={"name": name, "start_date": start_date, "end_date": end_date},
        )

    def get_seasons(self) -> Response:
        return self.client.get("/seasons")

    def get_season(self, season_id: int) -> Response:
        return self.client.get(f"/seasons/{season_id}")

    def update_season(self, season_id: int, name: str, start_date: str, end_date: str) -> Response:
        return self.client.put(
            url=f"/seasons/{season_id}",
            json={"name": name, "start_date": start_date, "end_date": end_date},
        )

    def delete_season(self, season_id: int) -> Response:
        return self.client.delete(f"/seasons/{season_id}")

    def create_mission(
        self,
        title: str,
        description: str,
        reward_xp: int,
        reward_mana: int,
        rank_requirement: int,
        season_id: int,
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
                "seasonId": season_id,
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
        season_id: int,
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
                "seasonId": season_id,
                "category": category,
            },
        )

    def delete_mission(self, mission_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}")

    def add_competency_reward_to_mission(
        self,
        mission_id: int,
        competency_id: int,
        level_increase: int,
    ) -> Response:
        return self.client.post(
            f"/missions/{mission_id}/competencies/{competency_id}",
            json={"level_increase": level_increase},
        )

    def remove_competency_reward_from_mission(
        self,
        mission_id: int,
        competency_id: int,
    ) -> Response:
        return self.client.delete(f"/missions/{mission_id}/competencies/{competency_id}")

    def add_skill_reward_to_mission(
        self,
        mission_id: int,
        skill_id: int,
        level_increase: int,
    ) -> Response:
        return self.client.post(
            f"/missions/{mission_id}/skills/{skill_id}",
            json={"level_increase": level_increase},
        )

    def remove_skill_reward_from_mission(self, mission_id: int, skill_id: int) -> Response:
        return self.client.delete(f"/missions/{mission_id}/skills/{skill_id}")

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
        rarity: ArtifactRarityEnum,
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

    def create_competency(self, name: str, max_level: int) -> Response:
        return self.client.post(
            url="/competencies",
            json={"name": name, "max_level": max_level},
        )

    def get_competencies(self) -> Response:
        return self.client.get("/competencies")

    def get_competency(self, competency_id: int) -> Response:
        return self.client.get(f"/competencies/{competency_id}")

    def update_competency(self, competency_id: int, name: str, max_level: int) -> Response:
        return self.client.put(
            url=f"/competencies/{competency_id}",
            json={"name": name, "max_level": max_level},
        )

    def delete_competency(self, competency_id: int) -> Response:
        return self.client.delete(f"/competencies/{competency_id}")

    def add_skill_to_competency(self, competency_id: int, skill_id: int) -> Response:
        return self.client.post(f"/competencies/{competency_id}/skills/{skill_id}")

    def remove_skill_from_competency(self, competency_id: int, skill_id: int) -> Response:
        return self.client.delete(f"/competencies/{competency_id}/skills/{skill_id}")

    def create_rank(self, name: str, required_xp: int) -> Response:
        return self.client.post(
            url="/ranks",
            json={"name": name, "required_xp": required_xp},
        )

    def get_ranks(self) -> Response:
        return self.client.get("/ranks")

    def get_rank(self, rank_id: int) -> Response:
        return self.client.get(f"/ranks/{rank_id}")

    def update_rank(self, rank_id: int, name: str, required_xp: int) -> Response:
        return self.client.put(
            url=f"/ranks/{rank_id}",
            json={"name": name, "required_xp": required_xp},
        )

    def delete_rank(self, rank_id: int) -> Response:
        return self.client.delete(f"/ranks/{rank_id}")

    def add_required_mission_to_rank(self, rank_id: int, mission_id: int) -> Response:
        return self.client.post(f"/ranks/{rank_id}/missions/{mission_id}")

    def remove_required_mission_from_rank(self, rank_id: int, mission_id: int) -> Response:
        return self.client.delete(f"/ranks/{rank_id}/missions/{mission_id}")

    def add_required_competency_to_rank(
        self, rank_id: int, competency_id: int, min_level: int
    ) -> Response:
        return self.client.post(
            f"/ranks/{rank_id}/competencies/{competency_id}",
            json={"min_level": min_level},
        )

    def remove_required_competency_from_rank(self, rank_id: int, competency_id: int) -> Response:
        return self.client.delete(f"/ranks/{rank_id}/competencies/{competency_id}")

    def create_mission_chain(
        self, name: str, description: str, reward_xp: int, reward_mana: int
    ) -> Response:
        return self.client.post(
            url="/mission-chains",
            json={
                "name": name,
                "description": description,
                "reward_xp": reward_xp,
                "reward_mana": reward_mana,
            },
        )

    def get_mission_chains(self) -> Response:
        return self.client.get("/mission-chains")

    def get_mission_chain(self, chain_id: int) -> Response:
        return self.client.get(f"/mission-chains/{chain_id}")

    def update_mission_chain(
        self, chain_id: int, name: str, description: str, reward_xp: int, reward_mana: int
    ) -> Response:
        return self.client.put(
            url=f"/mission-chains/{chain_id}",
            json={
                "name": name,
                "description": description,
                "reward_xp": reward_xp,
                "reward_mana": reward_mana,
            },
        )

    def delete_mission_chain(self, chain_id: int) -> Response:
        return self.client.delete(f"/mission-chains/{chain_id}")

    def add_mission_to_chain(self, chain_id: int, mission_id: int) -> Response:
        return self.client.post(f"/mission-chains/{chain_id}/missions/{mission_id}")

    def remove_mission_from_chain(self, chain_id: int, mission_id: int) -> Response:
        return self.client.delete(f"/mission-chains/{chain_id}/missions/{mission_id}")

    def add_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> Response:
        return self.client.post(
            f"/mission-chains/{chain_id}/dependencies",
            json={
                "mission_id": mission_id,
                "prerequisite_mission_id": prerequisite_mission_id,
            },
        )

    def remove_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> Response:
        return self.client.request(
            "DELETE",
            f"/mission-chains/{chain_id}/dependencies",
            json={
                "mission_id": mission_id,
                "prerequisite_mission_id": prerequisite_mission_id,
            },
        )

    def update_mission_order_in_chain(
        self, chain_id: int, mission_id: int, new_order: int
    ) -> Response:
        return self.client.put(
            f"/mission-chains/{chain_id}/missions/{mission_id}/order",
            params={"new_order": new_order},
        )
