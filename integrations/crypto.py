from cryptography.fernet import Fernet
from django.conf import settings


def get_cipher():
    key = settings.SOCIAL_ENCRYPTION_KEY
    if not key:
        raise ValueError("SOCIAL_ENCRYPTION_KEY não configurada no .env")
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_token(token: str) -> str:
    cipher = get_cipher()
    return cipher.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    cipher = get_cipher()
    return cipher.decrypt(encrypted_token.encode()).decode()
