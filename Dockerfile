# Usamos una imagen oficial de Python, versión slim (ligera)
FROM python:3.12-slim

# Instala herramientas del sistema:
# - build-essential: Necesario para compilar algunas librerías de Python.
# - make: Para poder usar nuestro Makefile.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        make \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de dependencias para aprovechar el caché de Docker.
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código (que vivirá en la carpeta 'src')
COPY src ./src