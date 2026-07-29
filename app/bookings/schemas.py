"""Esquemas Pydantic de reservas."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingBase(BaseModel):
    """Campos comunes de una reserva."""

    guest_name: str
    guest_email: str
    check_in: date   # Pydantic valida el formato de fecha: AAAA-MM-DD
    check_out: date
    status: str = "confirmada"  # si no se envia, la reserva queda confirmada
    room_id: int


class BookingCreate(BookingBase):
    """Datos que se envian para crear una reserva (POST)."""

    pass


class BookingUpdate(BookingBase):
    """Datos que se envian para actualizar una reserva (PUT)."""

    pass


class BookingResponse(BookingBase):
    """Datos que la API devuelve.

    Incluye el id y el total_price, que se calcula en el servidor
    y por eso no aparece en los esquemas de entrada.
    """

    id: int
    total_price: int

    model_config = ConfigDict(from_attributes=True)
