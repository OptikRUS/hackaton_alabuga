from abc import ABCMeta, abstractmethod


class PasswordService(metaclass=ABCMeta):
    @abstractmethod
    def generate_password_hash(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password_hash(self, password: str, hashed_password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def encode(self, payload: dict) -> str:
        raise NotImplementedError
