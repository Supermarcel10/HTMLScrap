# import secrets
# from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
#
# from cryptography.fernet import Fernet
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives.asymmetric import rsa
#
# backend = default_backend()
# iterations = 100_000
#
# def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(), length=32, salt=salt,
#         iterations=iterations, backend=backend)
#     return b64e(kdf.derive(password))
#
# def password_encrypt(password: bytes, key: str, iterations: int = iterations) -> bytes:
#     salt = secrets.token_bytes(16)
#     key = _derive_key(key.encode(), salt, iterations)
#     return b64e(
#         b'%b%b%b' % (
#             salt,
#             iterations.to_bytes(4, 'big'),
#             b64d(Fernet(key).encrypt(password)),
#         )
#     )
#
# def password_decrypt(token: bytes, key: str) -> bytes:
#     decoded = b64d(token)
#     salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
#     iterations = int.from_bytes(iter, 'big')
#     key = _derive_key(key.encode(), salt, iterations)
#     return Fernet(key).decrypt(token)
#
# # with open('data/memployees.sportsdirectservices.com.txt', mode="w") as f:
# #     f.write(str(password_encrypt(bytes("usr", "utf-8"), "key"), "utf-8"))
# #     f.write("\n")
# #     f.write(str(password_encrypt(bytes("pass", "utf-8"), "key"), "utf-8"))
#
# data = open('data/memployees.sportsdirectservices.com.txt', mode="r").readlines()

# Python Windows alternative

# from pytimedinput import timedKey
#
# value, TOut = timedKey(prompt=">> ", timeOut=3, allowCharacters=["y", "n"])
# print(TOut)
# print(value)



# Linux alternative

# import sys
# from select import select
#
# timeout = 3
# print("Enter something:")
# rlist, _, _ = select([sys.stdin], [], [], timeout)
# if rlist:
#     s = sys.stdin.readline()
#     print(s)
# else:
#     print ("No input. Moving on...")