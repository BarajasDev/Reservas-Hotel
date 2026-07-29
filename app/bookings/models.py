"""
Modelo de la tabla "bookings" (reservas).

Cada reserva pertenece a una habitacion, por eso guarda una
llave foranea (room_id) que apunta a la tabla rooms.
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    """Tabla de reservas."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Datos de la persona que reserva.
    guest_name = Column(String, nullable=False)
    guest_email = Column(String, nullable=False)

    # Fechas de entrada y salida del huesped.
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    # Total a pagar. Lo calcula la API (noches x precio de la habitacion),
    # asi el usuario no puede enviar un precio inventado.
    total_price = Column(Integer, nullable=False)

    # Estado de la reserva: confirmada o cancelada.
    status = Column(String, nullable=False, default="confirmada")

    # Llave foranea: enlaza la reserva con la habitacion reservada.
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    # Relacion inversa para poder escribir reserva.room
    room = relationship("Room", back_populates="bookings")
