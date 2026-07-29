# Imagen base: Python 3.11 en su version ligera (slim).
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor.
WORKDIR /code

# Evita archivos .pyc y muestra los logs al instante en la consola.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Se copia primero requirements.txt para aprovechar la cache de Docker:
# si el archivo no cambia, no vuelve a instalar las librerias.
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Se copia el codigo de la aplicacion y la configuracion de Alembic
# (alembic.ini y la carpeta alembic son necesarios para las migraciones).
COPY ./app /code/app
COPY alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic

# Puerto en el que escucha la API dentro del contenedor.
EXPOSE 8000

# Comando por defecto: levanta el servidor Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
