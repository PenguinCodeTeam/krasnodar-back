from bcrypt import gensalt, hashpw
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())


def check_password(password: str, password_hash: bytes):
    return pwd_context.verify(password, password_hash.decode('utf-8'))
