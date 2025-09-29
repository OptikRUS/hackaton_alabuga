from dataclasses import dataclass


@dataclass
class StoreItem:
    id: int
    title: str
    price: int
    stock: int


@dataclass
class StoreItems:
    values: list[StoreItem]


@dataclass
class StorePurchase:
    user_login: str
    store_item_id: int
