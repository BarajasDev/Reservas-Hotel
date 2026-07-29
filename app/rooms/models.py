"""
Modelo de la tabla "rooms" (habitaciones).

Cada habitacion pertenece a un hotel, por eso guarda una
llave foranea (hotel_id) que apunta a la tabla hotels.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Room(Base):
    """Tabla de habitaciones."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    # Numero visible de la habitacion, por ejemplo "101".
    # Es texto porque puede llevar letras, como "A-12".
    number = Column(String, nullable=False)

    # Tipo de habitacion: sencilla, doble, suite, etc.
    room_type = Column(String, nullable=False)

    # Cuantas personas caben en la habitacion.
    capacity = Column(Integer, nullable=False)

    # Precio por noche.
    price = Column(Integer, nullable=False)

    # Indica si la habitacion esta disponible para rentarse.
    is_available = Column(Boolean, nullable=False, default=True)

    # Llave foranea: enlaza la habitacion con su hotel.
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)

    # Relacion inversa para poder escribir habitacion.hotel
    hotel = relationship("Hotel", back_populates="rooms")

    # Una habitacion puede tener muchas reservas.
    bookings = relationship("Booking", back_populates="room", cascade="all, delete")
