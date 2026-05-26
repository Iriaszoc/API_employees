#!/usr/bin/env bash
set -euo pipefail
API_URL=${API_URL:-http://localhost:8080}

echo "Usando API_URL=$API_URL"

FAIL=0
log() { echo "[TEST] $*"; }

http_code() {
  url="$1"; shift
  code=$(curl -s -o /tmp/resp.$$ -w "%{http_code}" "$url" "$@")
  echo "$code"
}

body() {
  cat /tmp/resp.$$
}

# Espera sencilla para que el servicio quede listo (ajustar si es necesario)
wait_for_api() {
  n=0
  until [ $n -ge 30 ]
  do
    code=$(http_code "$API_URL/empleados" -m 5 || echo 000)
    if [ "$code" = "200" ]; then
      log "API lista"
      return 0
    fi
    n=$((n+1))
    sleep 2
  done
  log "Timeout esperando API"
  return 1
}

wait_for_api || exit 1

TS=$(date +%s)
EMP_NO=$((TS % 10000000))

# Test 1: Listar empleados (GET /empleados) -> 200
log "1) GET /empleados"
code=$(http_code "$API_URL/empleados")
if [ "$code" != "200" ]; then
  echo "FAIL: /empleados returned $code"
  FAIL=1
fi

# Test 2: Crear empleado (POST /empleados) -> 201 or 200
log "2) POST /empleados (crear)"
json=$(cat <<EOF
{"emp_no": $EMP_NO, "birth_date": "1990-01-01", "first_name": "PabloTest", "last_name": "Reyes", "gender": "M", "hire_date": "2026-05-20"}
EOF
)
code=$(curl -s -o /tmp/resp.$$ -w "%{http_code}" -H "Content-Type: application/json" -d "$json" "$API_URL/empleados")
if [ "$code" != "201" ] && [ "$code" != "200" ]; then
  echo "FAIL: POST /empleados returned $code"
  cat /tmp/resp.$$ || true
  FAIL=1
else
  log "Creado empleado emp_no=$EMP_NO (status $code)"
fi

# Test 3: GET creado
log "3) GET /empleados/$EMP_NO"
code=$(http_code "$API_URL/empleados/$EMP_NO")
if [ "$code" != "200" ]; then
  echo "FAIL: GET created returned $code"
  FAIL=1
fi

# Test 4: PUT actualizar
log "4) PUT /empleados/$EMP_NO (actualizar)"
upjson='{"first_name":"PabloUpdated","last_name":"Reyes","gender":"M"}'
code=$(curl -s -o /tmp/resp.$$ -w "%{http_code}" -H "Content-Type: application/json" -d "$upjson" -X PUT "$API_URL/empleados/$EMP_NO")
if [ "$code" != "200" ] && [ "$code" != "204" ]; then
  echo "FAIL: PUT returned $code"
  cat /tmp/resp.$$ || true
  FAIL=1
fi

# Test 5: GET verificar update
log "5) GET verificar /empleados/$EMP_NO contiene PabloUpdated"
curl -s -o /tmp/resp.$$ "$API_URL/empleados/$EMP_NO"
if ! grep -q "PabloUpdated" /tmp/resp.$$; then
  echo "FAIL: update not reflected"
  cat /tmp/resp.$$ || true
  FAIL=1
fi

# Test 6: DELETE
log "6) DELETE /empleados/$EMP_NO"
code=$(curl -s -o /tmp/resp.$$ -w "%{http_code}" -X DELETE "$API_URL/empleados/$EMP_NO")
if [ "$code" != "204" ] && [ "$code" != "200" ]; then
  echo "FAIL: DELETE returned $code"
  cat /tmp/resp.$$ || true
  FAIL=1
fi

# Test 7: GET should return 404
log "7) GET /empleados/$EMP_NO -> 404"
code=$(http_code "$API_URL/empleados/$EMP_NO" )
if [ "$code" != "404" ]; then
  echo "FAIL: GET after delete returned $code"
  FAIL=1
fi

# Test 8: Final list ok
log "8) GET /empleados (final)"
code=$(http_code "$API_URL/empleados")
if [ "$code" != "200" ]; then
  echo "FAIL: final /empleados returned $code"
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  echo "ALL TESTS PASSED"
  exit 0
else
  echo "SOME TESTS FAILED"
  exit 1
fi
