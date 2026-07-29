"""
Endpoints CRUD de hoteles.

CRUD son las cuatro operaciones basicas:
Create (POST), Read (GET), Update (PUT) y Delete (DELETE).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from .models import Hotel
from .schemas import HotelCreate, HotelResponse, HotelUpdate

# APIRouter agrupa las rutas de este modulo.
# prefix: todas las rutas empiezan con /hotels
# tags:   agrupa los endpoints con ese titulo dentro de /docs
router = APIRouter(prefix="/hotels", tags=["Hoteles"])


@router.post("/", response_model=HotelResponse, status_code=201)
def crear_hotel(datos: HotelCreate, db: Session = Depends(get_db)):
    """Crea un hotel nuevo. Devuelve 201 Created."""
    # Revisa que no exista otro hotel con el mismo nombre.
    existe = db.query(Hotel).filter(Hotel.name == datos.name).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un hotel con ese nombre")

    hotel = Hotel(name=datos.name, city=datos.city)
    db.add(hotel)      # agrega el hotel a la sesion
    db.commit()        # guarda los cambios en PostgreSQL
    db.refresh(hotel)  # recarga el objeto para obtener el id que genero la base
    return hotel


@router.get("/", response_model=list[HotelResponse])
def listar_hoteles(db: Session = Depends(get_db)):
    """Devuelve la lista de todos los hoteles."""
    return db.query(Hotel).all()


@router.get("/{hotel_id}", response_model=HotelResponse)
def obtener_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Devuelve un solo hotel buscandolo por su id."""
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    return hotel


@router.put("/{hotel_id}", response_model=HotelResponse)
def actualizar_hotel(hotel_id: int, datos: HotelUpdate, db: Session = Depends(get_db)):
    """Actualiza el nombre y la ciudad de un hotel."""
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")

    # Revisa que el nombre nuevo no lo tenga ya otro hotel distinto.
    repetido = (
        db.query(Hotel)
        .filter(Hotel.name == datos.name, Hotel.id != hotel_id)
        .first()
    )
    if repetido:
        raise HTTPException(status_code=400, detail="Ya existe otro hotel con ese nombre")

    hotel.name = datos.name
    hotel.city = datos.city
    db.commit()
    db.refresh(hotel)
    return hotel


@router.delete("/{hotel_id}", status_code=204)
def eliminar_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Elimina un hotel junto con sus habitaciones. Devuelve 204 No Content."""
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")

    db.delete(hotel)
    db.commit()
