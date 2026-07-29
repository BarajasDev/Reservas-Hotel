"""
Punto de entrada de la API.

Este archivo crea la aplicacion de FastAPI y registra las rutas
de los tres modulos del proyecto: hoteles, habitaciones y reservas.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.hotels.routes import router as hotels_router

# Carga las variables del archivo .env.
load_dotenv()

# El titulo de la API se puede cambiar desde el .env sin tocar el codigo.
APP_TITLE = os.getenv("APP_TITLE", "API Reservas Hotel")

# Se crea la aplicacion. FastAPI genera automaticamente la
# documentacion interactiva (Swagger UI) en la ruta /docs.
app = FastAPI(
    title=APP_TITLE,
    description="API REST para administrar hoteles.",
    version="1.0.0",
)

# Se registran las rutas del modulo de hoteles.
# El prefijo /api/v1 es la version de la API, asi que las rutas
# quedan como /api/v1/hotels.
app.include_router(hotels_router, prefix="/api/v1")


@app.get("/", tags=["Inicio"])
def inicio():
    """Ruta de bienvenida para comprobar que la API esta funcionando."""
    return {
        "mensaje": "API de Reservas de Hotel funcionando correctamente",
        "documentacion": "/docs",
    }
