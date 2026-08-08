# API de Reservas de Hotel

API REST desarrollada con **FastAPI** para administrar hoteles, habitaciones y reservas.
Los datos se guardan en **PostgreSQL** usando **SQLAlchemy** y las tablas se crean con
migraciones de **Alembic**. Todo el proyecto se levanta con **Docker Compose**.

Proyecto academico de la materia de desarrollo backend.
Alumno: Jahaziel Barajas Avila — Grupo 07IDESVA.

---

## Tecnologias utilizadas

| Tecnologia | Para que se usa |
|---|---|
| FastAPI | Construir la API y generar la documentacion automatica |
| Uvicorn | Servidor que ejecuta la aplicacion |
| SQLAlchemy | ORM para trabajar con la base de datos desde Python |
| PostgreSQL | Base de datos |
| Alembic | Migraciones (crear y versionar las tablas) |
| Pydantic | Validar los datos de entrada y dar forma a las respuestas |
| python-dotenv | Leer la configuracion desde el archivo `.env` |
| python-jose | Generar y validar los tokens JWT del login |
| Passlib | Guardar las contrasenas con hash, nunca en texto plano |
| Docker / Docker Compose | Levantar la API y la base de datos con un solo comando |

---

## Requisitos previos

- **Docker Desktop** instalado y en ejecucion.
- **Git** para clonar el repositorio.

No hace falta instalar Python ni PostgreSQL en la computadora: todo corre dentro
de los contenedores.

---

## Instalacion y ejecucion

### 1. Clonar el repositorio

```bash
git clone https://github.com/BarajasDev/Reservas-Hotel.git
cd Reservas-Hotel
```

### 2. Crear el archivo de configuracion `.env`

El repositorio incluye la plantilla `.env.example`. Se copia con otro nombre:

```bash
# Windows (CMD o PowerShell)
copy .env.example .env

# Linux o macOS
cp .env.example .env
```

### 3. Levantar el proyecto

```bash
docker compose up --build
```

Ese comando hace tres cosas:

1. Construye la imagen de la API e inicia el contenedor de PostgreSQL.
2. Espera a que la base de datos este lista.
3. Aplica las migraciones de Alembic (`alembic upgrade head`) y arranca el servidor.

### 4. Abrir la documentacion interactiva

Cuando la consola muestre `Application startup complete`, abrir en el navegador:

- **Documentacion interactiva (Swagger UI): http://localhost:8000/docs**
- Documentacion alterna (ReDoc): http://localhost:8000/redoc
- Ruta de prueba: http://localhost:8000/

Desde `/docs` se pueden probar todos los endpoints sin necesidad de otro programa.

### 5. Detener el proyecto

```bash
# Detener los contenedores (los datos se conservan)
docker compose down

# Detener y borrar tambien los datos de la base
docker compose down -v
```

---

## Variables de entorno

Se configuran en el archivo `.env` (ver la plantilla `.env.example`):

| Variable | Descripcion |
|---|---|
| `POSTGRES_USER` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | Contrasena de PostgreSQL |
| `POSTGRES_DB` | Nombre de la base de datos |
| `DATABASE_URL` | Cadena de conexion que usa SQLAlchemy |
| `APP_TITLE` | Titulo que aparece en la documentacion |
| `JWT_SECRET_KEY` | Clave con la que se firman los tokens JWT |
| `JWT_ALGORITHM` | Algoritmo de firma del token (HS256) |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de vigencia del token antes de expirar |

El archivo `.env` **no se sube a GitHub** porque contiene contrasenas; por eso se
incluye `.env.example` como plantilla.

---

## Estructura del proyecto

El proyecto esta organizado por modulos: cada entidad tiene su propia carpeta
con sus tres archivos (modelo, esquemas y rutas).

```text
Reservas-Hotel/
├── app/
│   ├── main.py              # Crea la aplicacion y registra las rutas
│   ├── database.py          # Conexion a PostgreSQL con SQLAlchemy
│   │
│   ├── auth/                # Autenticacion JWT
│   │   ├── security.py      # Hash de contrasena y creacion/validacion del token
│   │   ├── dependencies.py  # Dependencia que protege los endpoints con JWT
│   │   ├── schemas.py       # Esquema de la respuesta del login
│   │   └── routes.py        # Endpoints de registro y login
│   │
│   ├── users/                # Modulo de usuarios
│   │   ├── models.py        # Tabla users
│   │   └── schemas.py       # Esquemas Pydantic
│   │
│   ├── hotels/              # Modulo de hoteles
│   │   ├── models.py        # Tabla hotels
│   │   ├── schemas.py       # Esquemas Pydantic
│   │   └── routes.py        # Endpoints CRUD
│   │
│   ├── rooms/               # Modulo de habitaciones
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routes.py
│   │
│   └── bookings/            # Modulo de reservas
│       ├── models.py
│       ├── schemas.py
│       └── routes.py
│
├── alembic/
│   ├── env.py               # Configuracion de Alembic
│   └── versions/            # Migraciones en orden
│       ├── 0001_crear_tabla_hotels.py
│       ├── 0002_crear_tabla_rooms.py
│       ├── 0003_crear_tabla_bookings.py
│       └── 0004_crear_tabla_users.py
│
├── alembic.ini
├── docker-compose.yml       # Servicios: api + db
├── Dockerfile               # Imagen de la API
├── requirements.txt         # Librerias de Python
├── .env.example             # Plantilla de variables de entorno
└── README.md
```

---

## Modelo de datos

Las tres tablas estan relacionadas en cadena:

```text
hotels (1) ─── (muchas) rooms (1) ─── (muchas) bookings
```

- Un **hotel** tiene muchas **habitaciones** (`rooms.hotel_id`).
- Una **habitacion** tiene muchas **reservas** (`bookings.room_id`).

---

## Endpoints de la API

Todas las rutas viven bajo el prefijo `/api/v1`. Las rutas de hoteles,
habitaciones y reservas requieren un token JWT (ver seccion de autenticacion).

### Autenticacion

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/auth/register` | Registrar un usuario nuevo |
| POST | `/api/v1/auth/login` | Iniciar sesion y obtener el token JWT |

### Hoteles

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/hotels/` | Crear un hotel |
| GET | `/api/v1/hotels/` | Listar todos los hoteles |
| GET | `/api/v1/hotels/{hotel_id}` | Obtener un hotel por id |
| PUT | `/api/v1/hotels/{hotel_id}` | Actualizar un hotel |
| DELETE | `/api/v1/hotels/{hotel_id}` | Eliminar un hotel |

### Habitaciones

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/rooms/` | Crear una habitacion |
| GET | `/api/v1/rooms/` | Listar todas las habitaciones |
| GET | `/api/v1/rooms/{room_id}` | Obtener una habitacion por id |
| PUT | `/api/v1/rooms/{room_id}` | Actualizar una habitacion |
| DELETE | `/api/v1/rooms/{room_id}` | Eliminar una habitacion |

### Reservas

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/bookings/` | Crear una reserva |
| GET | `/api/v1/bookings/` | Listar todas las reservas |
| GET | `/api/v1/bookings/{booking_id}` | Obtener una reserva por id |
| PUT | `/api/v1/bookings/{booking_id}` | Actualizar una reserva |
| DELETE | `/api/v1/bookings/{booking_id}` | Eliminar una reserva |

---

## Reglas de negocio

**Hoteles**
- No se permiten dos hoteles con el mismo nombre.

**Habitaciones**
- El hotel al que se asigna la habitacion debe existir.
- La capacidad debe ser mayor a 0 y el precio no puede ser negativo.
- No se repite el numero de habitacion dentro del mismo hotel.

**Reservas**
- La habitacion que se reserva debe existir.
- La fecha de salida debe ser posterior a la de entrada.
- Una habitacion no se puede reservar dos veces en fechas que se cruzan.
- El total se calcula en el servidor: `noches x precio por noche`.

**Autenticacion**
- No se permiten dos usuarios con el mismo correo.
- La contrasena se guarda con hash, nunca en texto plano.
- Los endpoints de hoteles, habitaciones y reservas piden un token JWT valido;
  sin el header `Authorization: Bearer <token>` responden `401 Unauthorized`.

---

## Autenticacion (JWT)

**1. Registrar un usuario** — `POST /api/v1/auth/register`

```json
{
  "email": "admin@hotel.com",
  "password": "password123"
}
```

**2. Iniciar sesion** — `POST /api/v1/auth/login` (formulario, no JSON)

En `/docs` el boton **Authorize** abre el mismo formulario: el correo va en
el campo `username`. La respuesta trae el `access_token`.

**3. Usar el token en los endpoints protegidos**

En `/docs` se pega el token en el boton **Authorize**. Desde otro cliente
se envia el header:

```
Authorization: Bearer <access_token>
```

Si el token no se envia, ya expiro (dura `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`,
30 minutos por defecto) o es invalido, la API responde `401 Unauthorized`.

---

## Ejemplo de uso

Los datos se pueden capturar desde `/docs`. Primero hay que registrar un
usuario, iniciar sesion y autorizar el token (ver seccion anterior); despues
se sigue este orden, porque cada entidad depende de la anterior.

**1. Crear un hotel** — `POST /api/v1/hotels/`

```json
{
  "name": "Hotel Real del Valle",
  "city": "Tijuana"
}
```

**2. Crear una habitacion** — `POST /api/v1/rooms/` (usando el `id` del hotel)

```json
{
  "number": "101",
  "room_type": "doble",
  "capacity": 2,
  "price": 1200,
  "is_available": true,
  "hotel_id": 1
}
```

**3. Crear una reserva** — `POST /api/v1/bookings/` (usando el `id` de la habitacion)

```json
{
  "guest_name": "Jahaziel Barajas",
  "guest_email": "jahaziel@correo.com",
  "check_in": "2026-08-10",
  "check_out": "2026-08-13",
  "status": "confirmada",
  "room_id": 1
}
```

La API responde con el `total_price` ya calculado: 3 noches x 1200 = **3600**.

---

## Comandos utiles de Alembic

Las migraciones se aplican solas al levantar el proyecto, pero tambien se pueden
ejecutar a mano dentro del contenedor:

```bash
# Aplicar todas las migraciones pendientes
docker compose exec api alembic upgrade head

# Ver en que migracion esta la base de datos
docker compose exec api alembic current

# Ver el historial de migraciones
docker compose exec api alembic history

# Crear una migracion nueva despues de cambiar un modelo
docker compose exec api alembic revision --autogenerate -m "descripcion del cambio"
```
