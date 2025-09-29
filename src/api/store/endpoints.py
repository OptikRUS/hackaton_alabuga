from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.openapi import openapi_extra
from src.api.store.schemas import (
    StoreItemCreateRequest,
    StoreItemResponse,
    StoreItemsResponse,
    StoreItemUpdateRequest,
)
from src.core.store.use_cases import (
    CreateStoreItemUseCase,
    DeleteStoreItemUseCase,
    GetStoreItemsUseCase,
    GetStoreItemUseCase,
    UpdateStoreItemUseCase,
)

router = APIRouter(tags=["store"], route_class=DishkaRoute)


@router.post(
    path="/store",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать товар в магазине",
    description="Создает новый товар в магазине",
)
async def create_store_item(
    user: FromDishka[JwtHRUser],
    body: StoreItemCreateRequest,
    use_case: FromDishka[CreateStoreItemUseCase],
) -> StoreItemResponse:
    _ = user
    store_item = await use_case.execute(store_item=body.to_schema())
    return StoreItemResponse.from_schema(store_item=store_item)


@router.get(
    path="/store",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список товаров",
    description="Возвращает все товары в магазине",
)
async def get_store_items(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetStoreItemsUseCase],
) -> StoreItemsResponse:
    _ = user
    store_items = await use_case.execute()
    return StoreItemsResponse.from_schema(store_items=store_items)


@router.get(
    path="/store/{store_item_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить товар по ID",
    description="Возвращает товар по его идентификатору",
)
async def get_store_item(
    user: FromDishka[JwtUser],
    store_item_id: int,
    use_case: FromDishka[GetStoreItemUseCase],
) -> StoreItemResponse:
    _ = user
    store_item = await use_case.execute(store_item_id=store_item_id)
    return StoreItemResponse.from_schema(store_item=store_item)


@router.put(
    path="/store/{store_item_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить товар",
    description="Обновляет информацию о товаре",
)
async def update_store_item(
    user: FromDishka[JwtHRUser],
    store_item_id: int,
    body: StoreItemUpdateRequest,
    use_case: FromDishka[UpdateStoreItemUseCase],
) -> StoreItemResponse:
    _ = user
    store_item = await use_case.execute(store_item=body.to_schema(store_item_id=store_item_id))
    return StoreItemResponse.from_schema(store_item=store_item)


@router.delete(
    path="/store/{store_item_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить товар",
    description="Удаляет товар из магазина",
)
async def delete_store_item(
    user: FromDishka[JwtHRUser],
    store_item_id: int,
    use_case: FromDishka[DeleteStoreItemUseCase],
) -> None:
    _ = user
    await use_case.execute(store_item_id=store_item_id)
