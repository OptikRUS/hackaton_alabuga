from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    NAME: str = "alabuga"
    VERSION: str = "0.1.0"
    ADDRESS: str = "0.0.0.0"  # noqa: S104 Possible binding to all interfaces
    PORT: int = 8080
    PROTOCOL: str = "http"

    model_config = SettingsConfigDict(env_prefix="APP_")

    @property
    def MEDIA_URL(self) -> str:  # noqa: N802
        return f"{self.PROTOCOL}://{self.ADDRESS}:{self.PORT}/media"


class DatabaseSettings(BaseSettings):
    PROTOCOL: str = "postgresql+asyncpg"
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: SecretStr = SecretStr("postgres")
    NAME: str = "alabuga"

    model_config = SettingsConfigDict(env_prefix="DB_")

    @property
    def URL(self) -> SecretStr:  # noqa: N802
        return SecretStr(
            f"{self.PROTOCOL}://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.NAME}",
        )


class AuthSettings(BaseSettings):
    PRIVATE_KEY: SecretStr = SecretStr("secret_key")
    PUBLIC_KEY: SecretStr = SecretStr("secret_key")
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_prefix="AUTH_")


class MinioSettings(BaseSettings):
    ENDPOINT: str = "http://localhost:9000"
    ACCESS_KEY: SecretStr = SecretStr("minio")
    SECRET_KEY: SecretStr = SecretStr("minio12345")
    REGION: str = "us-east-1"
    BUCKET: str = "alabuga"
    USE_SSL: bool = False
    ADDRESSING_STYLE: str = "path"  # or "virtual"

    model_config = SettingsConfigDict(env_prefix="S3_")


class LoggingConfig(BaseSettings):
    RENDER_JSON_LOGS: bool = False
    PATH: Path | None = None
    LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class Settings(BaseSettings):
    APP: AppSettings = AppSettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    AUTH: AuthSettings = AuthSettings()
    MINIO: MinioSettings = MinioSettings()
    LOGGER: LoggingConfig = LoggingConfig()


settings = Settings()
