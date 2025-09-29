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
