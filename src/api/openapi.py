from collections.abc import Callable
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.config.settings import settings


def generate_custom_openapi(app: FastAPI) -> Callable[[], dict[str, Any]]:
    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=settings.APP.NAME,
            version=settings.APP.VERSION,
            routes=app.routes,
        )

        openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
        openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Введите токен в формате: **Bearer <token>**",
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi


openapi_extra: dict[str, Any] = {"security": [{"BearerAuth": []}]}
