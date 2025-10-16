#!/usr/bin/env sh
set -e

# Script para levantar los contenedores y abrir una shell en el servicio 'backend'.
# Uso: sh ./scripts/enter_dev.sh  (o bash ./scripts/enter_dev.sh)

echo "-> Construyendo y arrancando los contenedores (detached)..."
docker compose up -d --build

echo "-> Entrando al contenedor 'backend' (shell)..."
docker compose exec backend sh