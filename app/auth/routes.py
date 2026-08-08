"""Endpoints de registro e inicio de sesion."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserResponse

from .schemas import TokenResponse
from .security import crear_token_acceso, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/register", response_model=UserResponse, status_code=201)
def registrar_usuario(datos: UserCreate, db: Session = Depends(get_db)):
    """Registra un usuario nuevo. El correo debe ser unico."""
    email = datos.email.strip().lower()

    existe = db.query(User).filter(User.email == email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")

    usuario = User(email=email, password_hash=hash_password(datos.password))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=TokenResponse)
def iniciar_sesion(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Inicia sesion con correo y contrasena y devuelve un token JWT.

    Swagger UI envia el correo en el campo "username" del formulario.
    """
    email = form_data.username.strip().lower()
    usuario = db.query(User).filter(User.email == email).first()

    credenciales_invalidas = HTTPException(
        status_code=401, detail="Correo o contrasena incorrectos"
    )

    if usuario is None or not verify_password(form_data.password, usuario.password_hash):
        raise credenciales_invalidas

    token = crear_token_acceso(usuario.id)
    return TokenResponse(access_token=token)
