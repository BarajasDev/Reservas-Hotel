"""
Esquemas Pydantic de hoteles.

Los esquemas cumplen dos funciones:
1. Validar los datos que llegan en las peticiones (entrada).
2. Definir exactamente que campos devuelve la API (salida).
"""

from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    """Campos comunes de un hotel."""

    name: str
    city: str


class HotelCreate(HotelBase):
    """Datos que se envian para crear un hotel (POST)."""

    pass


class HotelUpdate(HotelBase):
    """Datos que se envian para actualizar un hotel (PUT)."""

    pass


class HotelResponse(HotelBase):
    """Datos que la API devuelve: los campos base mas el id."""

    id: int

    # from_attributes permite construir la respuesta leyendo
    # directamente los atributos del objeto de SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)
