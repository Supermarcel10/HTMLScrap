from secrets import token_bytes
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

backend = default_backend()
iterations = 100_000


def _derive_key(password: bytes, salt: bytes, iterate: int = iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterate, backend=backend)
    return b64e(kdf.derive(password))


def encrypt(password: bytes, key: str, iterate: int = iterations) -> bytes:
    salt = token_bytes(16)
    key = _derive_key(key.encode(), salt, iterate)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterate.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(password)),
        )
    )


def decrypt(token: bytes, key: str) -> bytes:
    decoded = b64d(token)
    salt, iterate, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iterate, 'big')
    key = _derive_key(key.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
