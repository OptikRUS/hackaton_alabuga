from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import StreamingResponse

from src.api.auth.schemas import JwtUser
from src.api.media.schemas import FileObjectResponse
from src.api.openapi import openapi_extra
from src.services.minio import MinioService

router = APIRouter(tags=["media"], route_class=DishkaRoute)


@router.post(
    path="/media",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить файл",
    description="Загружает файл в систему хранения медиа",
)
async def upload_file(
    file: Annotated[UploadFile, File(...)],
    user: FromDishka[JwtUser],
    minio_service: FromDishka[MinioService],
) -> FileObjectResponse:
    _ = user
    file_object = await minio_service.upload_file_stream(
        file_name=file.filename or "unknown",
        file_stream=file.file,
        content_type=file.content_type,
        file_size=file.size,
    )
    return FileObjectResponse.from_schema(file_object=file_object)


@router.get(
    path="/media/{key:path}",
    openapi_extra=openapi_extra,
    summary="Скачать файл",
    description="Скачивает файл из системы хранения медиа по ключу",
)
async def download_file(
    key: str,
    user: FromDishka[JwtUser],
    minio_service: FromDishka[MinioService],
) -> StreamingResponse:
    _ = user
    file_metadata = await minio_service.get_file_metadata(key=key)
    file_stream = minio_service.download_file(key)
    content_disposition = (
        "inline" if file_metadata.media_type.startswith("image/") else "attachment"
    )
    return StreamingResponse(
        content=file_stream,
        media_type=file_metadata.media_type,
        headers={
            "Content-Disposition": f'{content_disposition}; filename="{key.rsplit("/", 1)[-1]}"',
            "Content-Length": str(file_metadata.file_size),
            "Cache-Control": "public, max-age=3600",
        },
    )
