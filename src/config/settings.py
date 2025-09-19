from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    NAME: str = "alabuga"
    VERSION: str = "0.1.0"
    ADDRESS: str = "0.0.0.0"  # noqa: S104 Possible binding to all interfaces
    PORT: int = 8080

    model_config = SettingsConfigDict(env_prefix="APP_")


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


class Settings(BaseSettings):
    APP: AppSettings = AppSettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    AUTH: AuthSettings = AuthSettings()


settings = Settings()
