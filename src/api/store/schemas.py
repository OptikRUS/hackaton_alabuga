from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.store.schemas import StoreItem, StoreItems, StorePurchase


class StoreItemCreateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название товара")
    price: int = Field(default=..., ge=0, description="Цена товара")
    stock: int = Field(default=..., ge=0, description="Количество на складе")

    def to_schema(self) -> StoreItem:
        return StoreItem(id=0, title=self.title, price=self.price, stock=self.stock)


class StoreItemUpdateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название товара")
    price: int = Field(default=..., ge=0, description="Цена товара")
    stock: int = Field(default=..., ge=0, description="Количество на складе")

    def to_schema(self, store_item_id: int) -> StoreItem:
        return StoreItem(id=store_item_id, title=self.title, price=self.price, stock=self.stock)


class StoreItemResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор товара")
    title: str = Field(default=..., description="Название товара")
    price: int = Field(default=..., description="Цена товара")
    stock: int = Field(default=..., description="Количество на складе")

    @classmethod
    def from_schema(cls, store_item: StoreItem) -> "StoreItemResponse":
        return cls(
            id=store_item.id,
            title=store_item.title,
            price=store_item.price,
            stock=store_item.stock,
        )


class StoreItemsResponse(BoundaryModel):
    values: list[StoreItemResponse]

    @classmethod
    def from_schema(cls, store_items: StoreItems) -> "StoreItemsResponse":
        return cls(
            values=[StoreItemResponse.from_schema(store_item=item) for item in store_items.values]
        )


class StorePurchaseRequest(BoundaryModel):
    store_item_id: int = Field(default=..., description="ID товара")

    def to_schema(self, user_login: str) -> StorePurchase:
        return StorePurchase(user_login=user_login, store_item_id=self.store_item_id)
