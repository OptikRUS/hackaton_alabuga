from src.core.exceptions import BaseExceptionError


class StoreItemNotFoundError(BaseExceptionError):
    detail: str = "STORE_ITEM_NOT_FOUND_ERROR"


class StoreItemTitleAlreadyExistError(BaseExceptionError):
    detail: str = "STORE_ITEM_TITLE_ALREADY_EXIST_ERROR"


class StoreItemInsufficientStockError(BaseExceptionError):
    detail: str = "STORE_ITEM_INSUFFICIENT_STOCK_ERROR"


class InsufficientManaError(BaseExceptionError):
    detail: str = "INSUFFICIENT_MANA_ERROR"
