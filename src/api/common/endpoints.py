from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="", tags=["default"])


@router.get(path="/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@router.get("/")
async def default_redirect() -> RedirectResponse:
    return RedirectResponse("/docs", status_code=status.HTTP_302_FOUND)
