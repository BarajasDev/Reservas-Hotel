"""
Configuracion de Alembic.

Alembic es la herramienta que crea y aplica las migraciones, es decir,
los archivos que van construyendo las tablas de la base de datos paso a paso.

Este archivo le indica a Alembic dos cosas:
1. Cuales son los modelos del proyecto (para comparar contra la base de datos).
2. Con que cadena de conexion debe conectarse.
"""

import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Objeto de configuracion que lee los valores de alembic.ini
config = context.config

# Configura los mensajes (logs) que Alembic muestra en la consola.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Se cargan las variables del .env y se toma la cadena de conexion.
# Asi la contrasena de la base de datos no queda escrita en alembic.ini.
load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Se importan la clase Base y TODOS los modelos del proyecto.
# Si un modelo no se importa aqui, Alembic no lo detecta.
from app.database import Base  # noqa: E402
from app.bookings.models import Booking  # noqa: E402, F401
from app.hotels.models import Hotel  # noqa: E402, F401
from app.rooms.models import Room  # noqa: E402, F401

# Metadata con la estructura de todas las tablas del proyecto.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Genera el SQL de las migraciones sin conectarse a la base de datos."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Se conecta a la base de datos y aplica las migraciones."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Alembic decide el modo segun como se ejecute el comando.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
