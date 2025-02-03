import bcrypt


def hash_password(password: str) -> bytes:
    """Хэширование пароля"""
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes


def check_password(password: str, hashed_password: bytes) -> bool:
    """Проверка пароля"""
    check = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return check
