"""
Esquemas Pydantic de usuarios.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Datos que se envian para registrar un usuario (POST)."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    """Datos que la API devuelve de un usuario. Nunca incluye la contrasena."""

    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
