FROM python:3.12-slim

# No escribir archivos pyc y salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar 'make' para poder usar 'make' dentro del contenedor (útil en dev)
# Nota: usamos --no-install-recommends para mantener la imagen pequeña
RUN apt-get update && apt-get install -y --no-install-recommends make && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar (aprovecha cache de docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .


# Comando por defecto: usa la variable PORT si está definida
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]