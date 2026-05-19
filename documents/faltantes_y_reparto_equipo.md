# Faltantes del proyecto y reparto de equipo — Guía paso a paso

> **Proyecto:** Sistema de Gestión de Empleados — API REST en Go + MySQL + Docker  
> **Repositorio base:** `reporox/API_employees`  
> **Nota:** La asignación puede cambiar por acuerdo del equipo. Esto es una guía detallada generada a partir del estado real del código.

---

## Estado actual del código (lo que Roxana ya hizo)

| Archivo | Estado |
|---|---|
| `main.go` | API REST en Go con 5 endpoints CRUD sobre la tabla `employees` |
| `docker-compose.yml` | Servicios `db` (MySQL 8.0) y `api` (Go) declarados |
| `Dockerfile` | Single-stage: imagen `golang:1.26-alpine`, descarga deps, compila el binario `main` y expone el puerto 8080 |
| `init-db/employees.sql` | Schema completo: tablas `employees`, `departments`, `dept_emp`, `dept_manager`, `titles`, `salaries` |
| `init-db/*.dump` | Datos reales de 300,024 empleados listos para cargar |
| `go.mod` | Módulo `api-employees`, Go 1.26.3, dependencias `gorilla/mux v1.8.1` y `go-sql-driver/mysql v1.10.0` |

### Endpoints ya funcionales

| Método | Ruta | Handler en `main.go` |
|---|---|---|
| GET | `/empleados` | `getEmpleados` — devuelve los primeros 10 |
| GET | `/empleados/{id}` | `getEmpleado` — busca por `emp_no` |
| POST | `/empleados` | `createEmpleado` — inserta nuevo registro |
| PUT | `/empleados/{id}` | `updateEmpleado` — actualiza `first_name`, `last_name`, `gender` |
| DELETE | `/empleados/{id}` | `deleteEmpleado` — elimina por `emp_no` |

### Problemas detectados en el código actual

1. **`updateEmpleado`** responde con texto plano (`fmt.Fprintf`) en lugar de JSON.
2. **`deleteEmpleado`** retorna `204 No Content` sin cuerpo de confirmación — correcto, pero inconsistente con el README.
3. **`createEmpleado`** no valida que los campos requeridos lleguen completos antes de insertar.
4. **`getEmpleado`** retorna `404` genérico de Go sin cuerpo JSON propio cuando no encuentra el empleado.
5. **`docker-compose.yml`** no tiene `healthcheck` en el servicio `db`, por lo que la API puede arrancar antes de que MySQL esté listo.
6. **`Dockerfile`** usa `golang:1.26-alpine` — esta etiqueta no es una versión estable publicada en Docker Hub. Debe cambiarse a `golang:1.22-alpine` (la estable actual) para que la imagen pueda construirse correctamente.
7. La DSN de conexión (`root:password123@tcp(db:3306)/employees`) está escrita fija en `main.go` en lugar de leerla desde variables de entorno.

---

## Reparto detallado por integrante

---

## Roxana Irías Hernández — Backend Go + Docker, MySQL y despliegue

**Carga: Alta** | **Plazo sugerido: 4–5 días**

### Objetivo
Dejar el backend sólido y el entorno Docker confiable: respuestas JSON homogéneas, códigos HTTP correctos, validaciones básicas, variables de entorno en lugar de credenciales duras, healthcheck en el servicio db, archivo .env protegido y el proceso de arranque documentado en DEPLOY.md.

### Pasos detallados

#### Paso 1 — Leer las variables de entorno en `main.go`
El DSN actualmente está fijo en el código. Cambiar para que lo lea del entorno (que ya está declarado en `docker-compose.yml`).

En `main.go`, función `main()`, reemplazar la línea:
```go
dsn := "root:password123@tcp(db:3306)/employees"
```
por:
```go
host     := getEnv("DB_HOST", "db")
user     := getEnv("DB_USER", "root")
password := getEnv("DB_PASSWORD", "password123")
name     := getEnv("DB_NAME", "employees")
dsn      := fmt.Sprintf("%s:%s@tcp(%s:3306)/%s", user, password, host, name)
```
Y agregar la función auxiliar al final del archivo:
```go
func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}
```
No olvidar agregar `"os"` al bloque de imports.

#### Paso 2 — Homogeneizar respuestas JSON en `updateEmpleado`
Actualmente devuelve texto plano. Cambiarlo para que responda JSON consistente:

```go
func updateEmpleado(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    params := mux.Vars(r)
    var e Empleado
    json.NewDecoder(r.Body).Decode(&e)

    query := "UPDATE employees SET first_name = ?, last_name = ?, gender = ? WHERE emp_no = ?"
    result, err := db.Exec(query, e.FirstName, e.LastName, e.Gender, params["id"])
    if err != nil {
        http.Error(w, `{"error":"error al actualizar"}`, 500)
        return
    }
    rows, _ := result.RowsAffected()
    if rows == 0 {
        http.NotFound(w, r)
        return
    }
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"message": "empleado actualizado correctamente"})
}
```

#### Paso 3 — Mejorar respuesta 404 en `getEmpleado`
Cambiar `http.NotFound(w, r)` por una respuesta JSON propia:
```go
if err != nil {
    w.WriteHeader(http.StatusNotFound)
    json.NewEncoder(w).Encode(map[string]string{"error": "empleado no encontrado"})
    return
}
```

#### Paso 4 — Agregar validación básica en `createEmpleado`
Antes de ejecutar el INSERT, verificar que los campos no estén vacíos:
```go
if e.FirstName == "" || e.LastName == "" || e.Gender == "" || e.BirthDate == "" || e.HireDate == "" {
    w.WriteHeader(http.StatusBadRequest)
    json.NewEncoder(w).Encode(map[string]string{"error": "todos los campos son requeridos"})
    return
}
```

#### Paso 5 — Corregir versión de Go en el Dockerfile
El `Dockerfile` actual usa `FROM golang:1.26-alpine`. Esa etiqueta no existe en Docker Hub. Cambiarla a `golang:1.22-alpine`:
```dockerfile
FROM golang:1.22-alpine
```
También actualizar `go.mod` para declarar `go 1.22` en lugar de `go 1.26.3`, ya que 1.26 no es una versión publicada de Go.

#### Paso 6 — Agregar `healthcheck` al servicio `db` en `docker-compose.yml`
Actualmente el servicio `api` arranca junto con `db` sin verificar si MySQL ya está aceptando conexiones. Esto causa que la API falle al inicio.

Modificar `docker-compose.yml`:
```yaml
services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: employees
      MYSQL_ROOT_PASSWORD: password123
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-ppassword123"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 60s

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: password123
      DB_NAME: employees

volumes:
  db_data:
```

#### Paso 7 — Mover credenciales a un archivo `.env`
Crear `.env` en la raíz del proyecto:
```
MYSQL_ROOT_PASSWORD=password123
DB_PASSWORD=password123
```
Actualizar `docker-compose.yml` para usar `${MYSQL_ROOT_PASSWORD}` y `${DB_PASSWORD}`.

Agregar `.env` al `.gitignore` (actualmente solo contiene `main`, `.exe` y `db_data/`):
```
main
.exe
db_data/
.env
```

#### Paso 8 — Crear `docker-compose.test.yml` para CI
Este compose es idéntico al de producción pero sin volúmenes persistentes:
```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: employees
      MYSQL_ROOT_PASSWORD: password123
    volumes:
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-ppassword123"]
      interval: 10s
      timeout: 5s
      retries: 15
      start_period: 90s

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: password123
      DB_NAME: employees
```

#### Paso 9 — Probar el arranque limpio
```bash
docker-compose down -v
docker-compose up --build
```
Esperar hasta ver:
```
db-1  | ready for connections
api-1 | Servidor Go corriendo en puerto 8080...
```

#### Paso 10 — Crear `DEPLOY.md`
Crear `DEPLOY.md` en la raíz del repositorio con:
- Requisitos: Docker Desktop instalado y corriendo.
- Comando de primer arranque.
- Cómo saber que el sistema está listo (mensajes de terminal esperados).
- Cómo parar el sistema (`docker-compose down`).
- Cómo limpiar completamente (`docker-compose down -v`).
- Nota sobre el tiempo de carga inicial (~5-10 min).
- Cómo correr el script de pruebas (`bash tests/test_api.sh`).

---

## Frida Paulina Sepúlveda Becerra — Interfaz grafica del cliente Python

**Carga: Media** | **Plazo sugerido: 3–4 dias**

### Objetivo
Construir la capa visual del cliente de escritorio en Python: la ventana principal con la tabla de empleados, los formularios de alta y edicion, y el manejo visual de errores. La capa de comunicacion HTTP (`api_client.py`) la implementa Pablo, quien ya conoce todos los endpoints por su trabajo de pruebas.

### Requisitos previos
- Python 3.10+ instalado.
- Libreria `tkinter` (viene incluida con Python en Windows/Linux).
- Libreria `requests`: instalar con `pip install requests`.
- La API debe estar corriendo en `http://localhost:8080`.
- Coordinar con Pablo para recibir `api_client.py` antes de conectar la UI.

### Pasos detallados

#### Paso 1 — Crear la estructura del proyecto cliente
Dentro del repositorio del proyecto, crear la carpeta:
```
reporox/API_employees/cliente_python/
├── main.py          <- Punto de entrada (Frida)
├── api_client.py    <- Capa HTTP (Pablo)
└── ui.py            <- Ventana e interfaz grafica (Frida)
```

#### Paso 2 — Implementar `ui.py` con Tkinter
La ventana principal debe mostrar:
- Una tabla (widget `Treeview`) con columnas: `emp_no`, `first_name`, `last_name`, `gender`, `birth_date`, `hire_date`.
- Un boton **Refrescar** que llame a `obtener_empleados()` y cargue los datos en la tabla.
- Un boton **Buscar por ID** que abra un dialogo pequeno para ingresar el `emp_no`.
- Un boton **Nuevo empleado** que abra un formulario con los 6 campos del modelo.
- Un boton **Editar** que lea el empleado seleccionado en la tabla y abra el formulario pre-relleno.
- Un boton **Eliminar** que pida confirmacion antes de llamar a `eliminar_empleado()`.
- Un area de mensajes (Label o StatusBar) que muestre errores de conexion en rojo.

#### Paso 3 — Manejo de errores de conexion
En cada llamada a `api_client.py` desde la UI, capturar las excepciones:
```python
try:
    empleados = obtener_empleados()
except requests.exceptions.ConnectionError:
    mostrar_error("No se pudo conectar con la API. Esta corriendo Docker?")
except requests.exceptions.Timeout:
    mostrar_error("La API tardo demasiado en responder.")
except requests.exceptions.HTTPError as e:
    mostrar_error(f"Error HTTP: {e.response.status_code}")
```

#### Paso 4 — Implementar `main.py`
```python
from ui import App
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
```

#### Paso 5 — Crear `requirements.txt`
```
requests>=2.31.0
```
Colocarlo en `cliente_python/`.

#### Paso 6 — Probar el flujo completo
Con Docker corriendo (`docker-compose up --build`) y `api_client.py` de Pablo disponible:
1. Abrir la app: `python main.py`
2. Refrescar lista → deben aparecer 10 empleados.
3. Buscar un empleado por su `emp_no` (ej. `10001`).
4. Crear un empleado nuevo con datos inventados.
5. Editar el empleado recien creado.
6. Eliminarlo y verificar que desaparece de la lista.

---

## Martha Elizabeth Castorena Rivera — Documentacion formal del proyecto

**Carga: Media** | **Plazo sugerido: 3–4 dias**

### Objetivo
Redactar la documentacion tecnica formal del proyecto: contrato de API, registro de cambios y README actualizado. Esta documentacion es la evidencia escrita del trabajo del equipo y la referencia que el profesor revisara.

### Pasos detallados

#### Paso 1 — Redactar el contrato API (`API_CONTRACT.md`)
Crear `API_CONTRACT.md` en la raiz del repositorio con la documentacion formal de cada endpoint. Para cada uno incluir metodo, ruta, cuerpo del request, codigos de respuesta y cuerpo de la respuesta con ejemplo JSON.

Documentar los 5 endpoints:
- GET /empleados
- GET /empleados/{id}
- POST /empleados
- PUT /empleados/{id}
- DELETE /empleados/{id}

Ejemplo de plantilla para cada endpoint:
```markdown
### GET /empleados/{id}
Descripcion: Obtiene un empleado por su numero de empleado.

Parametros de ruta:
- id (integer) - Numero de empleado (emp_no)

Respuestas:
| Codigo | Descripcion | Cuerpo |
|---|---|---|
| 200 | Empleado encontrado | {"emp_no":10001,"first_name":"...","last_name":"...","gender":"M","birth_date":"...","hire_date":"..."} |
| 404 | No encontrado | {"error":"empleado no encontrado"} |
```

#### Paso 2 — Crear `CHANGELOG.md`
Crear `CHANGELOG.md` en la raiz del repositorio:
```markdown
## [1.1.0] - 2026-05-XX
### Anadido
- Variables de entorno para la conexion a MySQL
- Healthcheck en docker-compose para el servicio db
- Cliente de escritorio en Python (carpeta cliente_python/)
- Validacion de campos en POST /empleados
- Script bash automatizado de pruebas (tests/test_api.sh)
- Workflow de GitHub Actions con notificacion de resultados
- Contrato de API documentado en API_CONTRACT.md
- DEPLOY.md con guia de arranque

### Corregido
- Respuesta de updateEmpleado ahora es JSON
- Respuesta 404 de getEmpleado ahora incluye cuerpo JSON
- Version de imagen Go en Dockerfile (1.22-alpine)
- .gitignore actualizado para incluir .env
```

#### Paso 3 — Actualizar el `README.md` principal
El `README.md` actual tiene el bloque de codigo incompleto (faltan las comillas de cierre). Corregir y agregar:
- Seccion **Requisitos previos**: Docker Desktop instalado.
- Seccion **Estructura del proyecto**: lista de archivos y carpetas.
- Seccion **Ejemplos de uso** con los curl de los 5 endpoints.
- Seccion **Pruebas**: instruccion para correr `bash tests/test_api.sh`.
- Enlace a `API_CONTRACT.md`.
- Enlace a `DEPLOY.md`.

#### Paso 4 — Verificar consistencia antes de entregar
- Los ejemplos JSON del `API_CONTRACT.md` deben coincidir con los campos reales del modelo (`emp_no`, `birth_date`, `first_name`, `last_name`, `gender`, `hire_date`).
- Los codigos HTTP documentados deben coincidir con los que devuelve el backend corregido por Roxana.
- El README no debe tener bloques de codigo sin cerrar.

---

## Pablo Alberto Reyes Gutierrez — Capa HTTP del cliente + Pruebas bash + CI

**Carga: Media** | **Plazo sugerido: 3–4 dias**

### Objetivo
Implementar la capa de comunicacion HTTP del cliente Python (`api_client.py`), crear el script bash automatizado de pruebas del CRUD y configurar el workflow de GitHub Actions para ejecutar esas pruebas en cada push/PR y notificar el resultado al equipo.

### Pasos detallados

#### Paso 1 — Implementar `api_client.py`
Este archivo abstrae todas las llamadas HTTP que la UI de Frida necesita. Colocarlo en `cliente_python/api_client.py`:
```python
import requests

BASE_URL = "http://localhost:8080"

def obtener_empleados():
    r = requests.get(f"{BASE_URL}/empleados", timeout=5)
    r.raise_for_status()
    return r.json()

def obtener_empleado(emp_no):
    r = requests.get(f"{BASE_URL}/empleados/{emp_no}", timeout=5)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def crear_empleado(datos: dict):
    r = requests.post(f"{BASE_URL}/empleados", json=datos, timeout=5)
    r.raise_for_status()
    return r.json()

def actualizar_empleado(emp_no, datos: dict):
    r = requests.put(f"{BASE_URL}/empleados/{emp_no}", json=datos, timeout=5)
    r.raise_for_status()
    return r.json()

def eliminar_empleado(emp_no):
    r = requests.delete(f"{BASE_URL}/empleados/{emp_no}", timeout=5)
    r.raise_for_status()
    return True
```
Una vez listo, compartirlo con Frida para que lo integre en la UI.

#### Paso 2 — Preparar el entorno de pruebas
1. Clonar o actualizar el repositorio local.
2. Ejecutar `docker-compose up --build` y esperar a que el sistema este listo.
3. Verificar que `curl` esta disponible (`curl --version`).

#### Paso 2 — Crear el script bash de pruebas automatizado

Crear el archivo `tests/test_api.sh` en la raíz del repositorio. Este script ejecuta todos los casos de prueba del CRUD, verifica los códigos HTTP obtenidos y reporta PASS/FAIL por caso:

```bash
#!/usr/bin/env bash
# tests/test_api.sh — Suite de pruebas de la API de empleados
set -euo pipefail

BASE_URL="${API_URL:-http://localhost:8080}"
PASS=0
FAIL=0

# Colores para la terminal
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

check() {
  local desc="$1"
  local expected="$2"
  local actual="$3"
  if [ "$actual" -eq "$expected" ]; then
    echo -e "${GREEN}[PASS]${NC} $desc (HTTP $actual)"
    PASS=$((PASS + 1))
  else
    echo -e "${RED}[FAIL]${NC} $desc — esperado HTTP $expected, obtenido HTTP $actual"
    FAIL=$((FAIL + 1))
  fi
}

echo "================================================"
echo " Suite de pruebas — API Empleados"
echo " URL base: $BASE_URL"
echo "================================================"

# Caso 1 — Listar empleados (GET /empleados → 200)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/empleados")
check "GET /empleados lista empleados" 200 "$HTTP"

# Caso 2 — Obtener empleado existente (GET /empleados/10001 → 200)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/empleados/10001")
check "GET /empleados/10001 empleado existente" 200 "$HTTP"

# Caso 3 — Obtener empleado inexistente (GET /empleados/999999 → 404)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/empleados/999999")
check "GET /empleados/999999 empleado inexistente" 404 "$HTTP"

# Caso 4 — Crear empleado válido (POST /empleados → 201)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/empleados" \
  -H "Content-Type: application/json" \
  -d '{"emp_no":999001,"birth_date":"1990-01-15","first_name":"Test","last_name":"Usuario","gender":"M","hire_date":"2024-01-01"}')
check "POST /empleados crea empleado válido" 201 "$HTTP"

# Caso 5 — Crear empleado con datos incompletos (POST → 400)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/empleados" \
  -H "Content-Type: application/json" \
  -d '{"emp_no":999002,"first_name":"Incompleto"}')
check "POST /empleados rechaza datos incompletos" 400 "$HTTP"

# Caso 6 — Actualizar empleado existente (PUT /empleados/999001 → 200)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE_URL/empleados/999001" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"TestActualizado","last_name":"Apellido","gender":"F"}')
check "PUT /empleados/999001 actualiza empleado" 200 "$HTTP"

# Caso 7 — Eliminar empleado (DELETE /empleados/999001 → 204)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/empleados/999001")
check "DELETE /empleados/999001 elimina empleado" 204 "$HTTP"

# Caso 8 — Verificar que fue eliminado (GET /empleados/999001 → 404)
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/empleados/999001")
check "GET /empleados/999001 confirma eliminación" 404 "$HTTP"

echo "================================================"
echo " Resultado: $PASS PASS | $FAIL FAIL"
echo "================================================"

# Salir con error si hubo fallos (para que GitHub Actions lo detecte)
[ "$FAIL" -eq 0 ] || exit 1
```

Darle permisos de ejecución:
```bash
chmod +x tests/test_api.sh
```

Ejecutarlo localmente (con Docker corriendo):
```bash
bash tests/test_api.sh
```

#### Paso 3 — Pruebas de integración entre cliente y API
Una vez que Frida tenga el cliente listo:
1. Abrir la app de escritorio Python.
2. Realizar los mismos casos de prueba (1 al 8) desde la interfaz gráfica.
3. Verificar que los errores se muestran correctamente en la UI.
4. Documentar cualquier discrepancia entre el comportamiento de la API y el cliente.

#### Paso 4 — Pruebas de integracion entre cliente y API
Una vez que Frida tenga el cliente listo:
1. Abrir la app de escritorio Python.
2. Realizar los mismos casos de prueba (1 al 8) desde la interfaz grafica.
3. Verificar que los errores se muestran correctamente en la UI.
4. Documentar cualquier discrepancia entre el comportamiento de la API y el cliente y comunicarsela a Martha para actualizar el API_CONTRACT.md.

---

## GitHub Actions — CI con pruebas bash y notificación de resultados

> **Responsable:** Pablo (crea el workflow) + Martha (valida que docker-compose.test.yml arranque en CI)

### Objetivo
Ejecutar automáticamente el script `tests/test_api.sh` en cada push/PR, mostrar el resultado de cada caso (PASS/FAIL) en el log de GitHub Actions y enviar una notificación con el resumen.

### Paso 1 — Crear `docker-compose.test.yml`
Este compose es idéntico al de producción pero **sin volúmenes persistentes** (para que cada ejecución de CI arranque desde cero):

```yaml
# docker-compose.test.yml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: employees
      MYSQL_ROOT_PASSWORD: password123
    volumes:
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-ppassword123"]
      interval: 10s
      timeout: 5s
      retries: 15
      start_period: 90s

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: password123
      DB_NAME: employees
```

### Paso 2 — Crear el workflow `.github/workflows/tests.yml`

Crear la carpeta `.github/workflows/` en la raíz del repositorio y dentro el archivo `tests.yml`:

```yaml
name: "Pruebas API - CRUD Empleados"

on:
  push:
    branches: ["main", "master", "develop"]
  pull_request:
    branches: ["main", "master"]

jobs:
  test-api:
    name: "Pruebas de integracion con bash"
    runs-on: ubuntu-latest

    steps:
      # 1. Descargar el codigo
      - name: "Checkout del repositorio"
        uses: actions/checkout@v4

      # 2. Levantar la base de datos y la API con Docker Compose
      - name: "Levantar servicios (DB + API)"
        run: |
          docker compose -f docker-compose.test.yml up --build -d
          echo "Servicios iniciados. Esperando healthcheck..."

      # 3. Esperar a que la API responda (max. 3 min)
      - name: "Esperar a que la API este disponible"
        run: |
          echo "Esperando API en http://localhost:8080/empleados ..."
          for i in $(seq 1 36); do
            if curl -sf http://localhost:8080/empleados > /dev/null 2>&1; then
              echo "API disponible tras $((i * 5)) segundos."
              break
            fi
            echo "  intento $i/36 - reintentando en 5s..."
            sleep 5
          done
          curl -sf http://localhost:8080/empleados > /dev/null || (echo "API no respondio a tiempo." && exit 1)

      # 4. Ejecutar el script bash de pruebas
      - name: "Ejecutar pruebas bash (test_api.sh)"
        id: run_tests
        run: |
          chmod +x tests/test_api.sh
          bash tests/test_api.sh 2>&1 | tee test_output.txt
          echo "exit_code=${PIPESTATUS[0]}" >> $GITHUB_OUTPUT

      # 5. Subir el log de pruebas como artefacto descargable
      - name: "Guardar log de pruebas como artefacto"
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: resultados-pruebas
          path: test_output.txt
          retention-days: 7

      # 6. Mostrar resumen en la pestana Summary de GitHub Actions
      - name: "Publicar resumen de pruebas"
        if: always()
        run: |
          echo "## Resultado de Pruebas API" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo '```' >> $GITHUB_STEP_SUMMARY
          cat test_output.txt >> $GITHUB_STEP_SUMMARY
          echo '```' >> $GITHUB_STEP_SUMMARY
          if grep -q "\[FAIL\]" test_output.txt; then
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "FALLO: Algunas pruebas fallaron. Revisar el log adjunto." >> $GITHUB_STEP_SUMMARY
          else
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "OK: Todas las pruebas pasaron correctamente." >> $GITHUB_STEP_SUMMARY
          fi

      # 7. Bajar los servicios de Docker
      - name: "Detener servicios Docker"
        if: always()
        run: docker compose -f docker-compose.test.yml down -v

      # 8. Fallar el job si las pruebas no pasaron
      - name: "Verificar resultado final"
        if: always()
        run: |
          if grep -q "\[FAIL\]" test_output.txt; then
            echo "Pruebas fallidas detectadas."
            exit 1
          fi
          echo "Todas las pruebas pasaron."
```

### Paso 3 — Activar notificaciones en GitHub

Para que el equipo reciba notificaciones al completarse el workflow:

1. Ir al repositorio en GitHub > **Settings** > **Notifications**.
2. Verificar que cada integrante tenga activadas las notificaciones de **Actions** en su perfil: GitHub > Profile > Settings > Notifications > GitHub Actions > activar **"Failed workflows only"** o **"All"**.
3. El resumen de PASS/FAIL aparecerá automáticamente en la pestaña **"Summary"** de cada ejecución del workflow (Step 6 del workflow).
4. Si el workflow falla, GitHub marcará el PR/commit como fallido y enviará email de notificación.

### Paso 4 — Verificar que el workflow funciona
1. Hacer un commit con el workflow y el script en el mismo PR.
2. Ir a la pestaña **Actions** del repositorio en GitHub.
3. Abrir la ejecución más reciente → revisar el paso **"Ejecutar pruebas bash"**.
4. En la pestaña **Summary** debe aparecer la tabla de resultados PASS/FAIL.
5. El artefacto `resultados-pruebas` estará disponible para descarga durante 7 días.

---

## Resumen de entregables por persona

| Persona | Tarea principal | Archivos que entrega |
|---|---|---|
| Roxana Irias Hernandez | Backend Go + Docker/MySQL/Despliegue | `main.go`, `docker-compose.yml`, `docker-compose.test.yml`, `.env`, `.gitignore`, `DEPLOY.md` |
| Martha Elizabeth Castorena Rivera | Documentacion formal | `API_CONTRACT.md`, `CHANGELOG.md`, `README.md` |
| Frida Paulina Sepulveda Becerra | Interfaz grafica del cliente Python | `cliente_python/ui.py`, `main.py`, `requirements.txt` |
| Pablo Alberto Reyes Gutierrez | Capa HTTP + Pruebas bash + CI/CD | `cliente_python/api_client.py`, `tests/test_api.sh`, `.github/workflows/tests.yml` |

---

## Prioridad de ejecucion

1. **Roxana** termina primero el backend y Docker → los demas dependen de que la API arranque limpia y estable.
2. **Pablo** implementa `api_client.py` en paralelo con Roxana → Frida necesita este archivo para conectar la UI.
3. **Frida** construye la interfaz grafica → puede avanzar con la estructura de ventanas antes de recibir `api_client.py`.
4. **Martha** redacta la documentacion en paralelo → puede avanzar con el codigo existente sin esperar al cliente.
5. **Pablo** finaliza el script de pruebas y el workflow de CI una vez que Roxana tenga `docker-compose.test.yml` listo.

## Distribucion de carga

| Persona | Tarea | Carga | Plazo |
|---|---|---|---|
| Roxana Irias Hernandez | Backend + Docker/MySQL/Despliegue | Alta | 4-5 dias |
| Martha Elizabeth Castorena Rivera | Documentacion formal | Media | 3-4 dias |
| Frida Paulina Sepulveda Becerra | Interfaz grafica Python | Media | 3-4 dias |
| Pablo Alberto Reyes Gutierrez | api_client.py + Pruebas + CI | Media | 3-4 dias |
