"""Esquemas Pydantic de habitaciones."""

from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    """Campos comunes de una habitacion."""

    number: str
    room_type: str
    capacity: int
    price: int
    is_available: bool = True  # si no se envia, se asume disponible
    hotel_id: int


class RoomCreate(RoomBase):
    """Datos que se envian para crear una habitacion (POST)."""

    pass


class RoomUpdate(RoomBase):
    """Datos que se envian para actualizar una habitacion (PUT)."""

    pass


class RoomResponse(RoomBase):
    """Datos que la API devuelve: los campos base mas el id."""

    id: int

    model_config = ConfigDict(from_attributes=True)
