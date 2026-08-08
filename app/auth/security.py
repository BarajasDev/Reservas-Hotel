"""
Funciones de seguridad: hash de contrasenas y manejo del token JWT.
"""

import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# pbkdf2_sha256 no depende de librerias con codigo en C como bcrypt,
# asi que funciona sin problemas dentro del contenedor de Docker.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave-secreta-de-desarrollo")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def hash_password(password: str) -> str:
    """Convierte una contrasena en texto plano en su hash para guardarla."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Compara una contrasena en texto plano contra su hash guardado."""
    return pwd_context.verify(password, password_hash)


def crear_token_acceso(user_id: int) -> str:
    """Genera el JWT que el usuario debe enviar en los siguientes requests."""
    expira = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_token = {"sub": str(user_id), "exp": expira}
    return jwt.encode(datos_token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Valida el JWT y devuelve su contenido. Lanza JWTError si es invalido o expiro."""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
