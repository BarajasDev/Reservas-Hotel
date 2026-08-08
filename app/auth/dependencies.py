"""
Dependencia para proteger endpoints con JWT.

Se usa con Depends() en los routers que requieren que el usuario
haya iniciado sesion.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.users.models import User

from .security import decodificar_token

# tokenUrl le indica a Swagger UI en donde se obtiene el token (boton Authorize).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Valida el token JWT y devuelve el usuario autenticado.

    Se usa como dependencia de los routers de hoteles, habitaciones y
    reservas para exigir un token valido antes de dejar pasar la peticion.
    """
    error_credenciales = HTTPException(
        status_code=401,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decodificar_token(token)
    except JWTError:
        raise error_credenciales

    user_id = payload.get("sub")
    if user_id is None:
        raise error_credenciales

    usuario = db.query(User).filter(User.id == int(user_id)).first()
    if usuario is None or not usuario.is_active:
        raise error_credenciales

    return usuario
