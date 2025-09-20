from fastapi import APIRouter

from src.api.common import endpoints as common
from src.api.media import endpoints as media
from src.api.missions import endpoints as missions
from src.api.tasks import endpoints as tasks
from src.api.users import endpoints as users

root_router = APIRouter()
root_router.include_router(common.router, include_in_schema=False)
root_router.include_router(users.router)
root_router.include_router(missions.router)
root_router.include_router(tasks.router)
root_router.include_router(media.router)
