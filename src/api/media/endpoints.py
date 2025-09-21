from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import StreamingResponse

from src.api.media.schemas import FileObjectResponse
from src.services.minio import MinioService

router = APIRouter(tags=["media"], route_class=DishkaRoute)


@router.post(path="/media", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: Annotated[UploadFile, File(...)],
    minio_service: FromDishka[MinioService],
) -> FileObjectResponse:
    file_object = await minio_service.upload_file_stream(
        file_name=file.filename or "unknown",
        file_stream=file.file,
        content_type=file.content_type,
        file_size=file.size,
    )
    return FileObjectResponse.from_schema(file_object=file_object)


@router.get(path="/media/{key:path}")
async def download_file(
    key: str,
    minio_service: FromDishka[MinioService],
) -> StreamingResponse:
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
