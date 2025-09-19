from dataclasses import dataclass

import bcrypt
import jwt as pyjwt

from src.config.settings import settings
from src.core.password import PasswordService
from src.core.users.exceptions import UserIncorrectCredentialsError


@dataclass
class UserPasswordService(PasswordService):
    private_key: str = settings.AUTH.PRIVATE_KEY.get_secret_value()
    algorithm: str = settings.AUTH.ALGORITHM

    def generate_password_hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        password_bytes = password.encode("utf-8")
        hash_password = bcrypt.hashpw(password=password_bytes, salt=salt)
        return hash_password.decode("utf-8")

    def verify_password_hash(self, password: str, hashed_password: str) -> None:
        password_bytes = password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")
        if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
            raise UserIncorrectCredentialsError

    def encode(self, payload: dict) -> str:
        return pyjwt.encode(payload, key=self.private_key, algorithm=self.algorithm)
