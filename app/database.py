"""
Conexion a la base de datos con SQLAlchemy.

Aqui se prepara todo lo necesario para hablar con PostgreSQL:
el motor de conexion, la fabrica de sesiones y la clase base
de la que heredan los modelos (las tablas).
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Lee el archivo .env y carga sus valores como variables de entorno.
load_dotenv()

# La cadena de conexion NO se escribe en el codigo: viene del archivo .env.
# Ejemplo: postgresql://usuario:password@db:5432/reservas_hotel
DATABASE_URL = os.getenv("DATABASE_URL")

# El "engine" es el objeto que abre la conexion real con PostgreSQL.
engine = create_engine(DATABASE_URL)

# Fabrica de sesiones. Una sesion es la conversacion con la base de datos
# donde se hacen las consultas y se guardan los cambios.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Clase base de la que heredan todos los modelos del proyecto.
# Alembic la usa para saber que tablas debe crear en las migraciones.
Base = declarative_base()


def get_db():
    """Entrega una sesion de base de datos y la cierra al terminar.

    FastAPI la inyecta en cada endpoint con Depends(get_db), asi que
    cada peticion trabaja con su propia sesion y no se quedan
    conexiones abiertas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
