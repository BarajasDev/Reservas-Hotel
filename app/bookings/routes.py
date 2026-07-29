"""Endpoints CRUD de reservas."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.rooms.models import Room

from .models import Booking
from .schemas import BookingCreate, BookingResponse, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["Reservas"])

# Estados que acepta la API para una reserva.
ESTADOS_VALIDOS = ["confirmada", "cancelada"]


def validar_reserva(db: Session, datos, booking_id: int | None = None) -> Room:
    """Revisa las reglas de negocio y devuelve la habitacion reservada.

    Se usa al crear (POST) y al actualizar (PUT). El parametro booking_id
    sirve para no comparar la reserva contra si misma al editarla.
    """
    # La fecha de salida tiene que ser posterior a la de entrada.
    if datos.check_out <= datos.check_in:
        raise HTTPException(
            status_code=400,
            detail="La fecha de salida debe ser posterior a la de entrada",
        )

    # El estado debe ser uno de los permitidos.
    if datos.status not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="El estado solo puede ser 'confirmada' o 'cancelada'",
        )

    # La habitacion que se quiere reservar debe existir.
    habitacion = db.query(Room).filter(Room.id == datos.room_id).first()
    if habitacion is None:
        raise HTTPException(status_code=404, detail="La habitacion indicada no existe")

    # Una habitacion no se puede reservar dos veces en las mismas fechas.
    # Hay choque de fechas cuando la reserva existente empieza antes de que
    # termine la nueva y termina despues de que la nueva empieza.
    # Las reservas canceladas no ocupan la habitacion, por eso se ignoran.
    if datos.status == "confirmada":
        consulta = db.query(Booking).filter(
            Booking.room_id == datos.room_id,
            Booking.status == "confirmada",
            Booking.check_in < datos.check_out,
            Booking.check_out > datos.check_in,
        )
        if booking_id is not None:
            consulta = consulta.filter(Booking.id != booking_id)

        if consulta.first():
            raise HTTPException(
                status_code=400,
                detail="La habitacion ya esta reservada en esas fechas",
            )

    return habitacion


def calcular_total(datos, habitacion: Room) -> int:
    """Calcula el total de la reserva: noches x precio por noche."""
    noches = (datos.check_out - datos.check_in).days
    return noches * habitacion.price


@router.post("/", response_model=BookingResponse, status_code=201)
def crear_reserva(datos: BookingCreate, db: Session = Depends(get_db)):
    """Crea una reserva nueva y calcula su total."""
    habitacion = validar_reserva(db, datos)

    reserva = Booking(
        guest_name=datos.guest_name,
        guest_email=datos.guest_email,
        check_in=datos.check_in,
        check_out=datos.check_out,
        total_price=calcular_total(datos, habitacion),
        status=datos.status,
        room_id=datos.room_id,
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.get("/", response_model=list[BookingResponse])
def listar_reservas(db: Session = Depends(get_db)):
    """Devuelve la lista de todas las reservas."""
    return db.query(Booking).all()


@router.get("/{booking_id}", response_model=BookingResponse)
def obtener_reserva(booking_id: int, db: Session = Depends(get_db)):
    """Devuelve una sola reserva buscandola por su id."""
    reserva = db.query(Booking).filter(Booking.id == booking_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@router.put("/{booking_id}", response_model=BookingResponse)
def actualizar_reserva(booking_id: int, datos: BookingUpdate, db: Session = Depends(get_db)):
    """Actualiza una reserva y vuelve a calcular su total."""
    reserva = db.query(Booking).filter(Booking.id == booking_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    habitacion = validar_reserva(db, datos, booking_id=booking_id)

    reserva.guest_name = datos.guest_name
    reserva.guest_email = datos.guest_email
    reserva.check_in = datos.check_in
    reserva.check_out = datos.check_out
    reserva.total_price = calcular_total(datos, habitacion)
    reserva.status = datos.status
    reserva.room_id = datos.room_id
    db.commit()
    db.refresh(reserva)
    return reserva


@router.delete("/{booking_id}", status_code=204)
def eliminar_reserva(booking_id: int, db: Session = Depends(get_db)):
    """Elimina una reserva. Devuelve 204 No Content."""
    reserva = db.query(Booking).filter(Booking.id == booking_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    db.delete(reserva)
    db.commit()
