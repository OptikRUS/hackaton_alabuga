import aioboto3
from aiobotocore.client import BaseClient

from src.config.settings import settings

_minio_session = aioboto3.Session()


def get_minio_client() -> BaseClient:
    minio_client: BaseClient = _minio_session.client(
        service_name="s3",
        endpoint_url=settings.MINIO.ENDPOINT,
        aws_access_key_id=settings.MINIO.ACCESS_KEY.get_secret_value(),
        aws_secret_access_key=settings.MINIO.SECRET_KEY.get_secret_value(),
        region_name=settings.MINIO.REGION,
        use_ssl=settings.MINIO.USE_SSL,
    )
    return minio_client
