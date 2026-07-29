"""
Modelo de la tabla "hotels".

Un modelo de SQLAlchemy es una clase de Python que representa
una tabla de la base de datos. Cada atributo es una columna.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
    """Tabla de hoteles."""

    __tablename__ = "hotels"

    # Llave primaria: identificador unico que PostgreSQL genera solo.
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del hotel. unique=True evita registrar dos veces el mismo.
    name = Column(String, nullable=False, unique=True)

    # Ciudad donde se encuentra el hotel.
    city = Column(String, nullable=False)

    # Relacion uno a muchos: un hotel tiene muchas habitaciones.
    # Con cascade="all, delete", al borrar un hotel se borran
    # tambien las habitaciones que le pertenecen.
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete")
