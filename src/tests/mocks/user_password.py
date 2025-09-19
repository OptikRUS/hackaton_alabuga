from dataclasses import dataclass

from src.core.password import PasswordService
from src.core.users.exceptions import UserIncorrectCredentialsError


@dataclass
class UserPasswordServiceMock(PasswordService):
    def generate_password_hash(self, password: str) -> str:
        return password

    def verify_password_hash(self, password: str, hashed_password: str) -> None:
        if password != hashed_password:
            raise UserIncorrectCredentialsError

    def encode(self, payload: dict) -> str:
        return f"{payload}"
