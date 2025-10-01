from dataclasses import dataclass


@dataclass
class StoreItem:
    id: int
    title: str
    price: int
    stock: int
    image_url: str


@dataclass
class StoreItems:
    values: list[StoreItem]


@dataclass
class StorePurchase:
    user_login: str
    store_item_id: int
