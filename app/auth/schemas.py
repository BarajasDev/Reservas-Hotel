"""
Esquemas Pydantic de autenticacion.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Respuesta del login: el token JWT que se debe usar en los demas endpoints."""

    access_token: str
    token_type: str = "bearer"
