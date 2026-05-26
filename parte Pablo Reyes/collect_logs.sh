#!/usr/bin/env bash
# Guarda logs de los servicios docker-compose en logs_$(date).txt
ROOT="$(cd "$(dirname "$0")"/.. >/dev/null && pwd)"
COMPOSE_FILE="$ROOT/API_employees/docker-compose.test.yml"
OUTFILE="$ROOT/parte Pablo Reyes/logs_$(date +%Y%m%d_%H%M%S).txt"

docker-compose -f "$COMPOSE_FILE" logs --no-color > "$OUTFILE" || true

echo "Logs guardados en $OUTFILE"
