"""
Modelo de usuario.

Los usuarios son quienes pueden iniciar sesion y usar los endpoints
protegidos de hoteles, habitaciones y reservas.
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # El correo es la forma de identificar al usuario, por eso es unico.
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
