from fastapi import APIRouter

from src.api.artifacts import endpoints as artifacts
from src.api.common import endpoints as common
from src.api.competencies import endpoints as competencies
from src.api.media import endpoints as media
from src.api.mission_chains import endpoints as mission_chains
from src.api.missions import endpoints as missions
from src.api.ranks import endpoints as ranks
from src.api.seasons import endpoints as seasons
from src.api.skills import endpoints as skills
from src.api.tasks import endpoints as tasks
from src.api.users import endpoints as users

root_router = APIRouter()
root_router.include_router(common.router, include_in_schema=False)
root_router.include_router(users.router)
root_router.include_router(seasons.router)
root_router.include_router(missions.router)
root_router.include_router(mission_chains.router)
root_router.include_router(tasks.router)
root_router.include_router(competencies.router)
root_router.include_router(ranks.router)
root_router.include_router(skills.router)
root_router.include_router(artifacts.router)
root_router.include_router(media.router)
