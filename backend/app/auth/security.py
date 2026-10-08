from argon2 import PasswordHasher
from jose import jwt
from datetime import datetime, timedelta

password_hasher = PasswordHasher()

SECRET_KEY = "cybershield-secret-key-change-later"
ALGORITHM = "HS256"


def hash_password(password: str):
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str):
    try:
        password_hasher.verify(hashed_password, password)
        return True
    except Exception:
        return False


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )