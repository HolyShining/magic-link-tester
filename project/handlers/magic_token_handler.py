import json

from project.models import Tokens
from project import cipher


class MagicTokenHandler:
    @staticmethod
    def generate_token(email=None, **kwargs) -> Tokens:
        if email is None:
            raise ValueError("Email is required")

        payload = {"email": email}
        payload.update(kwargs)

        token = Tokens()
        token.email = email
        token.token = cipher.encrypt(json.dumps(payload)).decode()
        token.is_valid = True
        return token

    @classmethod
    def fetch_payload(cls, token=None) -> dict:
        if token is None:
            raise ValueError("Token is required")

        if cls.validate_token(token):
            return json.loads(cipher.decrypt(token.token.encode()))

    @staticmethod
    def validate_token(token=None) -> bool:
        if token is None:
            raise ValueError("Token is required")
        try:
            json.loads(cipher.decrypt(token.token.encode()))
        except Exception:
            return False
        return True

    @staticmethod
    def restore_token(token=None) -> str:
        if token is None:
            return ""
        if " " in token:
            token = token.replace(" ", "+")
        return token
