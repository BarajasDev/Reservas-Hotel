"""Endpoints CRUD de habitaciones."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.hotels.models import Hotel

from .models import Room
from .schemas import RoomCreate, RoomResponse, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Habitaciones"])


def validar_datos_habitacion(db: Session, datos, room_id: int | None = None):
    """Revisa las reglas de negocio antes de guardar una habitacion.

    Se usa tanto al crear (POST) como al actualizar (PUT). El parametro
    room_id sirve para excluir la habitacion que se esta editando
    cuando se busca un numero repetido.
    """
    # La capacidad y el precio deben tener valores logicos.
    if datos.capacity <= 0:
        raise HTTPException(status_code=400, detail="La capacidad debe ser mayor a 0")
    if datos.price < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo")

    # El hotel al que se quiere asignar la habitacion debe existir.
    hotel = db.query(Hotel).filter(Hotel.id == datos.hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="El hotel indicado no existe")

    # Dentro de un mismo hotel no puede repetirse el numero de habitacion.
    consulta = db.query(Room).filter(
        Room.hotel_id == datos.hotel_id,
        Room.number == datos.number,
    )
    if room_id is not None:
        consulta = consulta.filter(Room.id != room_id)

    if consulta.first():
        raise HTTPException(
            status_code=400,
            detail="Ese numero de habitacion ya existe en el hotel",
        )


@router.post("/", response_model=RoomResponse, status_code=201)
def crear_habitacion(datos: RoomCreate, db: Session = Depends(get_db)):
    """Crea una habitacion nueva dentro de un hotel."""
    validar_datos_habitacion(db, datos)

    habitacion = Room(
        number=datos.number,
        room_type=datos.room_type,
        capacity=datos.capacity,
        price=datos.price,
        is_available=datos.is_available,
        hotel_id=datos.hotel_id,
    )
    db.add(habitacion)
    db.commit()
    db.refresh(habitacion)
    return habitacion


@router.get("/", response_model=list[RoomResponse])
def listar_habitaciones(db: Session = Depends(get_db)):
    """Devuelve la lista de todas las habitaciones."""
    return db.query(Room).all()


@router.get("/{room_id}", response_model=RoomResponse)
def obtener_habitacion(room_id: int, db: Session = Depends(get_db)):
    """Devuelve una sola habitacion buscandola por su id."""
    habitacion = db.query(Room).filter(Room.id == room_id).first()
    if habitacion is None:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")
    return habitacion


@router.put("/{room_id}", response_model=RoomResponse)
def actualizar_habitacion(room_id: int, datos: RoomUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de una habitacion."""
    habitacion = db.query(Room).filter(Room.id == room_id).first()
    if habitacion is None:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")

    validar_datos_habitacion(db, datos, room_id=room_id)

    habitacion.number = datos.number
    habitacion.room_type = datos.room_type
    habitacion.capacity = datos.capacity
    habitacion.price = datos.price
    habitacion.is_available = datos.is_available
    habitacion.hotel_id = datos.hotel_id
    db.commit()
    db.refresh(habitacion)
    return habitacion


@router.delete("/{room_id}", status_code=204)
def eliminar_habitacion(room_id: int, db: Session = Depends(get_db)):
    """Elimina una habitacion. Devuelve 204 No Content."""
    habitacion = db.query(Room).filter(Room.id == room_id).first()
    if habitacion is None:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")

    db.delete(habitacion)
    db.commit()
