#!/usr/bin/env bash
set -euo pipefail
# Script para levantar el compose de pruebas y ejecutar el test suite localmente
ROOT="$(cd "$(dirname "$0")"/.. >/dev/null && pwd)"
# Asume que el archivo docker-compose.test.yml está en API_employees/
COMPOSE_FILE="$ROOT/API_employees/docker-compose.test.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "No se encontró $COMPOSE_FILE. Asegúrate de que exista."
  exit 1
fi

echo "Levantar servicios de prueba (docker-compose)"
docker-compose -f "$COMPOSE_FILE" up --build -d

echo "Esperando 10s para que los servicios inicialicen"
sleep 10

echo "Ejecutando tests"
"$ROOT/parte Pablo Reyes/tests/test_api.sh"

EXIT_CODE=$?

echo "Resultado tests: $EXIT_CODE"

echo "Bajando servicios"
docker-compose -f "$COMPOSE_FILE" down

exit $EXIT_CODE
