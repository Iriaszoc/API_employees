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

## Prioridad acordada para el cierre

1. Primero una interfaz sencilla que permita probar el avance real del backend sin esperar el producto final.
2. Después despliegue, GitHub Actions y verificación automatizada del flujo.
3. Las pruebas bash ya existen y funcionaron, así que se toman como base verificada y no como pendiente principal.

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
Construir la capa visual del cliente de escritorio en Python: una ventana sencilla pero funcional para listar, buscar, crear, editar y eliminar empleados sobre la API que ya existe.

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
├── main.py          <- Punto de entrada
├── api_client.py    <- Capa HTTP reutilizable
└── ui.py            <- Ventana e interfaz grafica sencilla
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

## Martha Elizabeth Castorena Rivera — Despliegue, pruebas y apoyo con GitHub Actions

**Carga: Media** | **Plazo sugerido: 3–4 dias**

### Objetivo
Apoyar el despliegue reproducible, investigar y dejar operativo GitHub Actions, revisar el flujo de pruebas y dejar evidencia clara de que el sistema levanta, responde y se puede verificar desde cero. No se trata de escribir documentacion larga, sino de hacer que el cierre tecnico sea reproducible y comprobable.

### Pasos detallados

#### Paso 1 — Validar el despliegue limpio
Probar que el proyecto levanta desde cero con Docker Compose sin depender de residuos de ejecuciones anteriores.

Checklist de esta verificacion:
- Arranque de MySQL sin errores.
- Arranque de la API solo cuando la BD ya este lista.
- Respuesta de `GET /empleados` desde `http://localhost:8080`.
- Apagado limpio con `docker-compose down`.

#### Paso 2 — Preparar el flujo de CI
Tomar el `docker-compose.test.yml` como base para automatizar pruebas en GitHub Actions.

Lo minimo que debe quedar listo:
- El workflow corre con `push` y `pull_request`.
- Levanta los servicios con el compose de prueba.
- Ejecuta el script bash de pruebas.
- Publica el resumen y los logs como evidencia.

#### Paso 3 — Revisar la evidencia de ejecucion
Guardar o revisar capturas, logs y resultados para demostrar que el proyecto no solo compila, sino que realmente funciona.

Evidencia esperada:
- salida del arranque en terminal,
- salida de `tests/test_api.sh`,
- log del workflow en GitHub Actions,
- artefacto descargable con resultados.

#### Paso 4 — Dar apoyo puntual a la integracion
Si al final hay diferencias entre lo que documenta la API y lo que responde en realidad, Eli apoya a detectar esas diferencias y las pasa al integrante que mantenga el contrato o la documentacion final.

#### Paso 5 — Cerrar pendientes de despliegue
Revisar que no queden detalles sueltos del entorno:
- rutas correctas en el workflow,
- nombres correctos de archivos en el repo,
- permisos de ejecucion para scripts bash,
- consistencia entre `docker-compose.yml` y `docker-compose.test.yml`.

### Entregables concretos
- `docker-compose.test.yml` validado.
- Workflow de GitHub Actions operativo.
- Logs de ejecucion guardados.
- Evidencia de pruebas y despliegue.
- Observaciones tecnicas de cualquier falla detectada en el flujo.

### Criterio de cierre
Eli termina su parte cuando el equipo puede levantar el entorno de forma repetible, ejecutar pruebas automatizadas y mostrar evidencia clara de que el sistema pasa por el flujo esperado sin depender de explicaciones verbales.

## Pablo Alberto Reyes Gutierrez — Capa HTTP del cliente + Pruebas bash + CI

**Carga: Media** | **Plazo sugerido: 3–4 dias**

### Objetivo
Implementar la capa de comunicacion HTTP del cliente Python (`api_client.py`) y dejar el flujo de pruebas conectado con el cliente. Las pruebas bash ya fueron hechas y funcionan, por lo que ahora se toman como soporte ya verificado.

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

#### Paso 2 — Asegurar la capa HTTP del cliente
Conectar el archivo `api_client.py` con la interfaz que se vaya a montar y dejar documentadas las funciones que ya consumen la API.

#### Paso 3 — Usar las pruebas bash como base verificada
Las pruebas bash ya existen y funcionaron, así que Pablo debe conservarlas como evidencia y adaptarlas solo si la API cambia.

#### Paso 4 — Pruebas de integracion entre cliente y API
Una vez que Frida tenga el cliente listo:
1. Abrir la app de escritorio Python.
2. Realizar los mismos casos de prueba (1 al 8) desde la interfaz grafica.
3. Verificar que los errores se muestran correctamente en la UI.
4. Documentar cualquier discrepancia entre el comportamiento de la API y el cliente y comunicarsela a quien lleve la documentación mínima del cierre.

---

## GitHub Actions — CI con pruebas bash y notificación de resultados

> **Responsable:** Pablo (crea el workflow) + Eli (valida que docker-compose.test.yml arranque en CI)

### Objetivo
Ejecutar automáticamente el script `tests/test_api.sh` en cada push/PR, mostrar el resultado de cada caso (PASS/FAIL) en el log de GitHub Actions y dejar evidencia descargable del resumen.

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
2. Verificar que cada integrante tenga activadas las notificaciones de **Actions** en su perfil.
3. El resumen de PASS/FAIL aparecerá automáticamente en la pestaña **Summary** de cada ejecución del workflow.
4. Si el workflow falla, GitHub marcará el PR/commit como fallido y enviará la notificación correspondiente.

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
| Eli | Despliegue + GitHub Actions + apoyo a pruebas | `docker-compose.test.yml`, `.github/workflows/tests.yml`, logs y evidencia de ejecución |
| Frida Paulina Sepulveda Becerra | Interfaz grafica del cliente Python | `cliente_python/ui.py`, `main.py`, `requirements.txt` |
| Pablo Alberto Reyes Gutierrez | Capa HTTP + integración con interfaz | `cliente_python/api_client.py`, apoyo a pruebas de integración y evidencia |

---

## Prioridad de ejecucion

1. **Roxana** termina primero el backend y Docker → los demas dependen de que la API arranque limpia y estable.
2. **Frida** construye la interfaz grafica → puede avanzar con la estructura de ventanas mientras Pablo deja lista la capa HTTP.
3. **Pablo** ajusta `api_client.py` y deja la integración de cliente lista para probar.
4. **Eli** toma despliegue, GitHub Actions y evidencia para que el flujo quede reproducible.
5. Las pruebas bash ya se consideran base verificada y sirven como evidencia, no como bloqueo pendiente.

## Distribucion de carga

| Persona | Tarea | Carga | Plazo |
|---|---|---|---|
| Roxana Irias Hernandez | Backend + Docker/MySQL/Despliegue | Alta | 4-5 dias |
| Eli | Despliegue + GitHub Actions + evidencia | Media | 3-4 dias |
| Frida Paulina Sepulveda Becerra | Interfaz grafica Python | Media | 3-4 dias |
| Pablo Alberto Reyes Gutierrez | api_client.py + integración con interfaz | Media | 3-4 dias |
