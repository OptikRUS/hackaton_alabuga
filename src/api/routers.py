from fastapi import APIRouter

from src.api.common import endpoints as common
from src.api.users import endpoints as users

root_router = APIRouter()
root_router.include_router(common.router, include_in_schema=False)
root_router.include_router(users.router)
